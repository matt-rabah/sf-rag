from pathlib import Path
import json
import re
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHUNKS_FILE = PROJECT_ROOT / "data" / "chunks" / "grounding_chunks.jsonl"
EVALS_FILE = PROJECT_ROOT / "evals" / "retrieval_tests.jsonl"

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


def tokenize(text: str):
    words = re.findall(r"[A-Za-z0-9]+", text.lower())
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
    return len(overlap)


def run_retrieval_test(eval_record: dict, chunks: list):
    question = eval_record["question"]
    expected_source_id = eval_record["expected_source_id"]

    scored_chunks = [
        {
            "score": score_chunk(question, chunk),
            "chunk": chunk,
        }
        for chunk in chunks
    ]

    scored_chunks = sorted(scored_chunks, key=lambda item: item["score"], reverse=True)
    top_result = scored_chunks[0] if scored_chunks else None

    if not top_result or top_result["score"] == 0:
        return {
            "passed": False,
            "reason": "No matching chunk found.",
            "top_source_id": None,
            "top_chunk_id": None,
            "score": 0,
        }

    top_chunk = top_result["chunk"]
    top_source_id = top_chunk.get("source_id")

    return {
        "passed": top_source_id == expected_source_id,
        "reason": "Matched expected source." if top_source_id == expected_source_id else "Top source did not match expected source.",
        "top_source_id": top_source_id,
        "top_chunk_id": top_chunk.get("chunk_id"),
        "top_heading": top_chunk.get("chunk_heading"),
        "score": top_result["score"],
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
    print(f"Loaded {len(evals)} retrieval evals.\n")

    for eval_record in evals:
        result = run_retrieval_test(eval_record, chunks)

        status = "✅" if result["passed"] else "❌"

        print(f"{status} {eval_record['id']}: {eval_record['question']}")
        print(f"   Expected source: {eval_record['expected_source_id']}")
        print(f"   Top source:      {result['top_source_id']}")
        print(f"   Top chunk:       {result['top_chunk_id']}")
        print(f"   Top heading:     {result.get('top_heading')}")
        print(f"   Score:           {result['score']}")
        print(f"   Result:          {result['reason']}\n")

        if not result["passed"]:
            failures += 1

    if failures:
        print(f"❌ Retrieval tests failed: {failures}/{len(evals)}")
        return 1

    print(f"✅ All {len(evals)} retrieval tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())