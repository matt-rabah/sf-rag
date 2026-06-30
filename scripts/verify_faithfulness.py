"""Faithfulness verification for answers produced by answer_question.py.

Two layers, because they catch different failures:

1. Deterministic guard (no API key; always safe to run):
   - Invented citations: any URL or "[Source N]" reference the model emits that
     is not present in / exceeds the retrieved context. The grounding system
     prompt forbids inventing URLs; this enforces it.
   - Off-context answer: the chosen option's salient terms are largely absent
     from the retrieved context (the answer is about something that was not
     retrieved). This is a low-floor check — lexical overlap cannot tell a
     correct option from an in-vocabulary distractor (both score high), but it
     reliably flags an answer that is grounded in nothing.

2. LLM entailment judge (opt-in, needs the model):
   A strict second pass that decides whether the retrieved context actually
   supports the chosen answer and names the supporting source. This is the real
   entailment check; the deterministic layer only guards the obvious failures.

The verdict text from the answerer is never rewritten — faithfulness findings are
appended as a clearly marked caution so the study answer stays intact.
"""

from pathlib import Path
import json
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_keyword_retrieval import tokenize  # noqa: E402

ANSWER_RE = re.compile(r"Answer:\s*\**\s*([A-E])\b", re.IGNORECASE)
CONFIDENCE_RE = re.compile(r"Confidence:\s*\**\s*(\d{1,2})", re.IGNORECASE)
URL_RE = re.compile(r"https?://[^\s)\]}>\"']+")
SOURCE_REF_RE = re.compile(r"\bSource\s+(\d+)\b", re.IGNORECASE)
OPTION_RE = re.compile(r"^\s*\**\s*([A-E])\s*[.):]\s*(.+?)\s*$")

# Chosen option whose terms overlap the context below this fraction is flagged as
# "off-context". Calibrated against the labeled set, where correct answers score
# >= 0.89; a low floor only fires on genuinely ungrounded answers.
OFF_CONTEXT_FLOOR = 0.34

REFUSAL_MARKER = "i don't have enough source-backed information"


def parse_answer(answer_text: str) -> dict:
    refused = REFUSAL_MARKER in answer_text.lower()
    letter = ANSWER_RE.search(answer_text)
    conf = CONFIDENCE_RE.search(answer_text)
    return {
        "refused": refused,
        "letter": letter.group(1).upper() if letter else None,
        "confidence": int(conf.group(1)) if conf else None,
    }


def extract_options(question_text: str) -> dict:
    """Parse lettered options ('A. ...', 'B) ...', 'C: ...') from a question."""
    options = {}
    for line in question_text.splitlines():
        m = OPTION_RE.match(line)
        if m:
            options[m.group(1).upper()] = m.group(2).strip()
    return options


def grounding_score(text: str, context: str) -> float:
    terms = set(tokenize(text))
    if not terms:
        return 1.0
    ctx = set(tokenize(context))
    return len(terms & ctx) / len(terms)


def find_unsupported_citations(answer_text: str, context: str, n_sources: int) -> dict:
    bad_urls = [u for u in URL_RE.findall(answer_text) if u not in context]
    bad_refs = sorted(
        {int(n) for n in SOURCE_REF_RE.findall(answer_text) if int(n) < 1 or int(n) > n_sources}
    )
    return {"urls": bad_urls, "source_refs": bad_refs}


def count_sources(context: str) -> int:
    return len(re.findall(r"\[Source\s+\d+\]", context))


def deterministic_assess(answer_text: str, question_text: str, context: str) -> dict:
    """Run the keyless guard. Returns parsed answer plus any cautions."""
    parsed = parse_answer(answer_text)
    cautions = []

    if parsed["refused"]:
        return {**parsed, "cautions": [], "faithful": True}

    n_sources = count_sources(context)
    bad = find_unsupported_citations(answer_text, context, n_sources)
    if bad["urls"]:
        cautions.append(
            "referenced URL(s) not in the retrieved context: " + ", ".join(bad["urls"])
        )
    if bad["source_refs"]:
        cautions.append(
            "referenced source number(s) outside the retrieved context: "
            + ", ".join(f"Source {n}" for n in bad["source_refs"])
        )

    options = extract_options(question_text)
    chosen = parsed["letter"]
    if chosen and chosen in options:
        gs = grounding_score(options[chosen], context)
        if gs < OFF_CONTEXT_FLOOR:
            cautions.append(
                f"the chosen answer ({chosen}) barely overlaps the retrieved context "
                f"(grounding {gs:.0%}) — it may not be source-backed"
            )

    return {**parsed, "cautions": cautions, "faithful": not cautions}


def caution_block(cautions: list) -> str:
    lines = "\n".join(f"- {c}" for c in cautions)
    return (
        "\n\n⚠ Faithfulness check flagged this answer; verify against the source:\n"
        f"{lines}"
    )


# --- Optional LLM entailment judge ---------------------------------------------

VERIFIER_SYSTEM = (
    "You are a strict grounding verifier. Using ONLY the provided context, decide "
    "whether it directly supports the proposed answer. Do not use outside "
    "knowledge. If the context does not directly state or clearly imply the "
    "answer, 'supported' must be false."
)


def build_verifier_prompt(context: str, question: str, letter: str, option_text: str) -> str:
    return (
        "Retrieved context:\n"
        f"{context}\n\n"
        "Question:\n"
        f"{question}\n\n"
        f"Proposed answer: {letter}. {option_text}\n\n"
        'Respond with ONE line of JSON and nothing else: '
        '{"supported": true|false, "source": <the Source number that supports it, or null>, '
        '"reason": "<one short phrase>"}'
    )


def parse_verdict(text: str) -> dict:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return {"supported": None, "source": None, "reason": "unparseable verdict"}
    try:
        data = json.loads(match.group(0))
    except json.JSONDecodeError:
        return {"supported": None, "source": None, "reason": "unparseable verdict"}
    return {
        "supported": data.get("supported"),
        "source": data.get("source"),
        "reason": str(data.get("reason", "")),
    }


def llm_verify(client, model: str, context: str, question: str, letter: str, option_text: str) -> dict:
    response = client.messages.create(
        model=model,
        max_tokens=512,
        system=VERIFIER_SYSTEM,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": build_verifier_prompt(context, question, letter, option_text)}
                ],
            }
        ],
    )
    text = "".join(b.text for b in response.content if b.type == "text")
    return parse_verdict(text)
