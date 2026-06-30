"""Answer-quality eval harness for the SF-RAG study tool.

This is the scoreboard for the answering pipeline. It runs labeled multiple-choice
questions (evals/answer_tests.jsonl) through the same retrieval + gate + answer
path as scripts/answer_question.py and reports how good the tool actually is.

Two layers of checks:

  Structural (no API key required) — for every labeled question:
    - source_retrieved: the labelled supporting source is actually retrieved.
    - answerable: the relevance gate would NOT refuse (the question is
      answerable from the corpus). A refusal here means a retrieval/coverage gap.
  These catch retrieval regressions deterministically and run in CI without a key.

  Model (requires ANTHROPIC_API_KEY) — for every labeled question:
    - accuracy: does the model pick the labelled correct letter?
    - calibration: bucket answers by the model's self-reported confidence and
      compare each bucket's stated confidence to its real accuracy.
    - refusal rate on questions that are supposed to be answerable.

Usage:
  python3 scripts/test_answer_quality.py            # model run if a key is set, else structural only
  python3 scripts/test_answer_quality.py --no-model # structural checks only
  python3 scripts/test_answer_quality.py --prompt technical

Exit code is non-zero if any structural check fails (those are real bugs) or, in
a model run, if accuracy falls below --min-accuracy (default 0.8).
"""

from pathlib import Path
import argparse
import os
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_keyword_retrieval import load_jsonl, score_chunk  # noqa: E402
import answer_question as aq  # noqa: E402

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHUNKS_FILE = PROJECT_ROOT / "data" / "chunks" / "grounding_chunks.jsonl"
EVALS_FILE = PROJECT_ROOT / "evals" / "answer_tests.jsonl"

ANSWER_RE = re.compile(r"Answer:\s*\**\s*([A-E])\b", re.IGNORECASE)
CONFIDENCE_RE = re.compile(r"Confidence:\s*\**\s*(\d{1,2})", re.IGNORECASE)


def validate(records: list) -> list:
    errors = []
    seen = set()
    for i, r in enumerate(records, 1):
        rid = r.get("id", f"<line {i}>")
        if rid in seen:
            errors.append(f"{rid}: duplicate id")
        seen.add(rid)
        opts = r.get("options")
        if not isinstance(opts, dict) or len(opts) < 2:
            errors.append(f"{rid}: needs an 'options' object with >= 2 choices")
            continue
        if r.get("correct") not in opts:
            errors.append(f"{rid}: 'correct' ({r.get('correct')}) is not one of the options")
        for field in ("question", "expected_source_id", "exam_domain"):
            if not r.get(field):
                errors.append(f"{rid}: missing '{field}'")
    return errors


def question_text(record: dict) -> str:
    """Mimic a transcribed practice question: stem followed by lettered options."""
    lines = [record["question"], ""]
    for letter, text in record["options"].items():
        lines.append(f"{letter}. {text}")
    return "\n".join(lines)


def structural_check(record: dict, chunks: list) -> dict:
    results = aq.retrieve(question_text(record), chunks, aq.DEFAULT_TOP_K)
    _, sufficient = aq.build_retrieved_context(results)
    expected = record["expected_source_id"]
    source_retrieved = any(
        r["chunk"].get("source_id") == expected and r["score"] >= aq.MIN_CHUNK_SCORE
        for r in results
    )
    return {"answerable": sufficient, "source_retrieved": source_retrieved, "results": results}


def parse_answer(text: str) -> dict:
    refused = aq.REFUSAL_PHRASE.lower() in text.lower()
    letter = ANSWER_RE.search(text)
    conf = CONFIDENCE_RE.search(text)
    return {
        "refused": refused,
        "letter": letter.group(1).upper() if letter else None,
        "confidence": int(conf.group(1)) if conf else None,
    }


def model_check(record: dict, results: list, client, prompt_name: str) -> dict:
    context, sufficient = aq.build_retrieved_context(results)
    if not sufficient:
        return {"refused": True, "letter": None, "confidence": None, "correct": False}
    prompt_text = aq.load_prompt(prompt_name, context)
    raw = aq.answer(client, prompt_text, question_text(record))
    parsed = parse_answer(raw)
    parsed["correct"] = parsed["letter"] == record["correct"] and not parsed["refused"]
    return parsed


def report_calibration(rows: list) -> None:
    # rows: list of (confidence, correct) for answered (non-refused) questions
    buckets = {"low (1-4)": [], "med (5-7)": [], "high (8-10)": [], "unknown": []}
    for conf, correct in rows:
        if conf is None:
            buckets["unknown"].append(correct)
        elif conf <= 4:
            buckets["low (1-4)"].append(correct)
        elif conf <= 7:
            buckets["med (5-7)"].append(correct)
        else:
            buckets["high (8-10)"].append(correct)
    print("\nConfidence calibration (stated confidence vs. actual accuracy):")
    for name, vals in buckets.items():
        if not vals:
            continue
        acc = sum(vals) / len(vals)
        print(f"  {name:12s} n={len(vals):2d}  accuracy={acc:5.0%}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Score the answering pipeline on labeled MCQs.")
    parser.add_argument("--no-model", action="store_true", help="Run structural checks only.")
    parser.add_argument("--prompt", choices=sorted(aq.PROMPT_TEMPLATES), default="scenario")
    parser.add_argument("--min-accuracy", type=float, default=0.8)
    args = parser.parse_args()

    records = load_jsonl(EVALS_FILE)
    errors = validate(records)
    if errors:
        print("❌ answer_tests.jsonl validation failed.")
        for e in errors:
            print(f"   - {e}")
        return 1

    chunks = load_jsonl(CHUNKS_FILE)
    print(f"Loaded {len(records)} answer-quality questions and {len(chunks)} chunks.\n")

    have_key = bool(os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN"))
    run_model = not args.no_model and have_key
    client = aq.make_client() if run_model else None
    if not run_model:
        why = "--no-model set" if args.no_model else "no ANTHROPIC_API_KEY"
        print(f"Model checks skipped ({why}); running structural checks only.\n")

    struct_failures = 0
    calib_rows = []
    answered = correct = refused = 0

    for r in records:
        s = structural_check(r, chunks)
        flags = []
        if not s["source_retrieved"]:
            flags.append("source NOT retrieved")
        if not s["answerable"]:
            flags.append("gate would REFUSE")
        struct_ok = not flags
        struct_failures += 0 if struct_ok else 1

        line = f"{'✅' if struct_ok else '❌'} {r['id']} [{r['exam_domain']}]"
        if flags:
            line += "  <- " + "; ".join(flags)

        if run_model:
            m = model_check(r, s["results"], client, args.prompt)
            if m["refused"]:
                refused += 1
                line += "  | model: REFUSED"
            else:
                answered += 1
                correct += int(m["correct"])
                calib_rows.append((m["confidence"], m["correct"]))
                mark = "✓" if m["correct"] else "✗"
                line += f"  | model: {m['letter']} (conf {m['confidence']}) want {r['correct']} {mark}"
        print(line)

    print(f"\nStructural: {len(records) - struct_failures}/{len(records)} passed "
          f"(source retrieved + answerable).")

    accuracy = None
    if run_model:
        accuracy = (correct / answered) if answered else 0.0
        print(f"Model: answered {answered}, refused {refused}, "
              f"accuracy {correct}/{answered} = {accuracy:.0%}.")
        report_calibration(calib_rows)

    failed = struct_failures > 0 or (accuracy is not None and accuracy < args.min_accuracy)
    if failed:
        msgs = []
        if struct_failures:
            msgs.append(f"{struct_failures} structural failure(s)")
        if accuracy is not None and accuracy < args.min_accuracy:
            msgs.append(f"accuracy {accuracy:.0%} < {args.min_accuracy:.0%}")
        print(f"\n❌ Answer-quality check failed: {', '.join(msgs)}.")
        return 1

    print("\n✅ Answer-quality checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
