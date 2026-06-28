from pathlib import Path
import json
import re
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHUNKS_FILE = PROJECT_ROOT / "data" / "chunks" / "grounding_chunks.jsonl"
EVALS_FILE = PROJECT_ROOT / "evals" / "retrieval_tests.jsonl"

TOP_K = 5

STOPWORDS = {
    "the",
    "a",
    "an",
    "and",
    "or",
    "but",
    "is",
    "are",
    "was",
    "were",
    "to",
    "of",
    "in",
    "on",
    "for",
    "with",
    "by",
    "from",
    "as",
    "at",
    "this",
    "that",
    "what",
    "which",
    "how",
    "does",
    "do",
    "it",
    "its",
}


def normalize_text(text: str):
    text = text.lower()
    text = text.replace("’", "'")
    text = text.replace("–", "-")
    text = text.replace("—", "-")
    text = re.sub(r"[*_`#>$begin:math:display$$end:math:display$():]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def tokenize(text: str):
    words = re.findall(r"[A-Za-z0-9]+", normalize_text(text))
    return [word for word in words if word not in STOPWORDS and len(word) > 1]


def load_jsonl(path: Path):
    records = []

    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")

    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if not line:
                continue

            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as error:
                raise ValueError(f"{path.name} line {line_number}: Invalid JSON: {error}")

    return records


def score_chunk(question: str, chunk: dict):
    query_terms = set(tokenize(question))
    exam_domain_terms = set(tokenize(chunk.get("exam_domain", "")))
    heading_terms = set(tokenize(chunk.get("chunk_heading", "")))
    topic_terms = set(tokenize(chunk.get("topic", "")))

    chunk_text = " ".join(
        [
            chunk.get("title", ""),
            chunk.get("exam_domain", ""),
            chunk.get("product_area", ""),
            chunk.get("topic", ""),
            chunk.get("chunk_heading", ""),
            chunk.get("chunk_text", ""),
        ]
    )

    chunk_terms = set(tokenize(chunk_text))

    if not query_terms:
        return 0

    overlap = query_terms.intersection(chunk_terms)

    score = len(overlap)

    # Boost chunks where the question overlaps with structured metadata.
    score += 2 * len(query_terms.intersection(exam_domain_terms))
    score += 2 * len(query_terms.intersection(heading_terms))
    score += 1 * len(query_terms.intersection(topic_terms))

    # Boost exam outline chunks for weighting/percentage questions.
    question_normalized = normalize_text(question)
    heading_normalized = normalize_text(chunk.get("chunk_heading", ""))

    if any(term in question_normalized for term in ["weight", "weighting", "percentage", "percent"]):
        if "%" in chunk.get("chunk_heading", "") or "%" in chunk.get("chunk_text", ""):
            score += 3

    # Boost chunks that look like exam outline sections.
    if re.search(r"\b\d{1,2}%\b", chunk.get("chunk_heading", "")):
        score += 2

    return score


def contains_any(text: str, expected_values: list):
    normalized = normalize_text(text)
    return any(normalize_text(str(value)) in normalized for value in expected_values)


def contains_all(text: str, expected_values: list):
    normalized = normalize_text(text)
    return all(normalize_text(str(value)) in normalized for value in expected_values)


def chunk_matches_expectation(chunk: dict, eval_record: dict):
    expected_source_id = eval_record["expected_source_id"]
    expected_heading_contains = eval_record.get("expected_heading_contains", [])
    expected_answer_contains = eval_record.get("expected_answer_contains", [])

    source_matches = chunk.get("source_id") == expected_source_id
    heading_matches = contains_any(chunk.get("chunk_heading", ""), expected_heading_contains)
    answer_terms_match = contains_all(chunk.get("chunk_text", ""), expected_answer_contains)

    return source_matches and heading_matches and answer_terms_match


def run_retrieval_test(eval_record: dict, chunks: list):
    question = eval_record["question"]

    scored_chunks = [
        {
            "score": score_chunk(question, chunk),
            "chunk": chunk,
        }
        for chunk in chunks
    ]

    scored_chunks = sorted(scored_chunks, key=lambda item: item["score"], reverse=True)
    top_results = scored_chunks[:TOP_K]

    matching_result = None

    for result in top_results:
        if chunk_matches_expectation(result["chunk"], eval_record):
            matching_result = result
            break

    top_result = top_results[0] if top_results else None

    if matching_result:
        matched_chunk = matching_result["chunk"]
        return {
            "passed": True,
            "reason": f"Expected answer-bearing chunk found in top {TOP_K}.",
            "matched_source_id": matched_chunk.get("source_id"),
            "matched_chunk_id": matched_chunk.get("chunk_id"),
            "matched_heading": matched_chunk.get("chunk_heading"),
            "matched_score": matching_result["score"],
            "top_source_id": top_result["chunk"].get("source_id") if top_result else None,
            "top_chunk_id": top_result["chunk"].get("chunk_id") if top_result else None,
            "top_heading": top_result["chunk"].get("chunk_heading") if top_result else None,
            "top_score": top_result["score"] if top_result else 0,
        }

    return {
        "passed": False,
        "reason": f"Expected answer-bearing chunk was not found in top {TOP_K}.",
        "matched_source_id": None,
        "matched_chunk_id": None,
        "matched_heading": None,
        "matched_score": 0,
        "top_source_id": top_result["chunk"].get("source_id") if top_result else None,
        "top_chunk_id": top_result["chunk"].get("chunk_id") if top_result else None,
        "top_heading": top_result["chunk"].get("chunk_heading") if top_result else None,
        "top_score": top_result["score"] if top_result else 0,
    }


def main():
    try:
        chunks = load_jsonl(CHUNKS_FILE)
        evals = load_jsonl(EVALS_FILE)
    except Exception as error:
        print(f"❌ {error}")
        return 1

    failures = 0

    print(f"Loaded {len(chunks)} chunks.")
    print(f"Loaded {len(evals)} retrieval evals.")
    print(f"Using top_k={TOP_K}.\n")

    for eval_record in evals:
        result = run_retrieval_test(eval_record, chunks)

        status = "✅" if result["passed"] else "❌"

        print(f"{status} {eval_record['id']}: {eval_record['question']}")
        print(f"   Expected source:    {eval_record['expected_source_id']}")
        print(f"   Expected heading:   {eval_record.get('expected_heading_contains')}")
        print(f"   Expected terms:     {eval_record.get('expected_answer_contains')}")
        print(f"   Top source:         {result['top_source_id']}")
        print(f"   Top chunk:          {result['top_chunk_id']}")
        print(f"   Top heading:        {result.get('top_heading')}")
        print(f"   Top score:          {result['top_score']}")
        print(f"   Matched chunk:      {result['matched_chunk_id']}")
        print(f"   Matched heading:    {result['matched_heading']}")
        print(f"   Matched score:      {result['matched_score']}")
        print(f"   Result:             {result['reason']}\n")

        if not result["passed"]:
            failures += 1

    if failures:
        print(f"❌ Retrieval tests failed: {failures}/{len(evals)}")
        return 1

    print(f"✅ All {len(evals)} retrieval tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())