"""Exam-coverage report: where the corpus and evals are thin vs. exam weight.

Maps the official exam blueprint (data/metadata/exam_domain_map.yaml) against what
is actually in the corpus and the eval suites, so you can see — per domain and per
topic — where to add real source material. It does not invent content; it tells
you where content is missing.

For each exam domain it shows the exam weight, the corpus share (docs/chunks), and
the number of retrieval and answer-quality evals, flagging domains that are
under-resourced relative to their weight. For each topic it reports whether any
chunk covers it, and lists the uncovered topics.

    python3 scripts/coverage_report.py

Runs without an API key.
"""

from pathlib import Path
import json
import sys

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_keyword_retrieval import load_jsonl, tokenize  # noqa: E402

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOMAIN_MAP = PROJECT_ROOT / "data" / "metadata" / "exam_domain_map.yaml"
CHUNKS_FILE = PROJECT_ROOT / "data" / "chunks" / "grounding_chunks.jsonl"
RETRIEVAL_EVALS = PROJECT_ROOT / "evals" / "retrieval_tests.jsonl"
ANSWER_EVALS = PROJECT_ROOT / "evals" / "answer_tests.jsonl"


def chunk_token_sets(chunks: list) -> dict:
    """domain -> list of token sets (one per chunk) for topic-coverage checks."""
    by_domain = {}
    for c in chunks:
        text = " ".join(
            str(c.get(f, ""))
            for f in ("title", "topic", "chunk_heading", "chunk_text")
        )
        by_domain.setdefault(c.get("exam_domain"), []).append(set(tokenize(text)))
    return by_domain


def topic_covered(topic: str, token_sets: list) -> bool:
    """A topic is covered if some chunk contains all of its content tokens."""
    terms = set(tokenize(topic))
    if not terms:
        return True
    return any(terms <= ts for ts in token_sets)


def count_by_domain(records: list) -> dict:
    counts = {}
    for r in records:
        counts[r.get("exam_domain")] = counts.get(r.get("exam_domain"), 0) + 1
    return counts


def main() -> int:
    domain_map = yaml.safe_load(DOMAIN_MAP.read_text(encoding="utf-8"))
    domains = domain_map["domains"]
    chunks = load_jsonl(CHUNKS_FILE)
    retrieval = load_jsonl(RETRIEVAL_EVALS)
    answers = load_jsonl(ANSWER_EVALS)

    tokens_by_domain = chunk_token_sets(chunks)
    docs_by_domain = {}
    for c in chunks:
        docs_by_domain.setdefault(c.get("exam_domain"), set()).add(c.get("source_id"))
    retr_counts = count_by_domain(retrieval)
    ans_counts = count_by_domain(answers)

    total_docs = sum(len(v) for v in docs_by_domain.values())

    print(f"Exam: {domain_map.get('certification')} ({domain_map.get('exam_version')})")
    print(f"Corpus: {len({c.get('source_id') for c in chunks})} sources, {len(chunks)} chunks\n")
    print(f"{'Domain':32s} {'wt%':>4} {'docs':>5} {'corpus%':>8} {'retr':>5} {'ans':>4}  balance")
    print("-" * 78)

    uncovered = []
    for d in domains:
        name = d["name"]
        weight = d.get("weight", 0)
        n_docs = len(docs_by_domain.get(name, set()))
        corpus_share = (100 * n_docs / total_docs) if total_docs else 0
        # "balance" compares corpus share to exam weight: under = thin vs weight.
        ratio = (corpus_share / weight) if weight else 0
        tag = "UNDER" if ratio < 0.8 else ("over" if ratio > 1.5 else "ok")
        print(
            f"{name:32s} {weight:>4} {n_docs:>5} {corpus_share:>7.0f}% "
            f"{retr_counts.get(name, 0):>5} {ans_counts.get(name, 0):>4}  {tag}"
        )

        token_sets = tokens_by_domain.get(name, [])
        missing = [t for t in d.get("topics", []) if not topic_covered(t, token_sets)]
        if missing:
            uncovered.append((name, weight, missing))

    print("\nUncovered exam topics (no chunk contains the topic's terms):")
    if not uncovered:
        print("  none — every listed topic has at least one matching chunk.")
    else:
        for name, weight, missing in sorted(uncovered, key=lambda x: -x[1]):
            print(f"\n  {name} ({weight}% of exam):")
            for t in missing:
                print(f"    - {t}")
        print(
            "\nThese are candidates for new official source documents. Add them via the "
            "ingestion workflow in README (manifest -> cleaned doc -> validate -> chunk)."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
