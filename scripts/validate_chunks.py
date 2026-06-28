from pathlib import Path
import json
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHUNKS_FILE = PROJECT_ROOT / "data" / "chunks" / "grounding_chunks.jsonl"

REQUIRED_FIELDS = [
    "chunk_id",
    "source_id",
    "title",
    "source_type",
    "source_url",
    "certification",
    "exam_domain",
    "product_area",
    "topic",
    "retrieved_date",
    "release_relevance",
    "authority",
    "status",
    "chunk_index",
    "chunk_heading",
    "chunk_text",
    "token_estimate",
]

ALLOWED_RELEASE_RELEVANCE = {
    "current",
    "needs_review",
    "archived",
    "deprecated",
}

ALLOWED_STATUS = {
    "active",
    "draft",
    "needs_review",
    "deprecated",
}

MIN_CHUNK_WORDS = 20
MAX_CHUNK_WORDS = 500


def validate_chunk(chunk: dict, line_number: int):
    errors = []

    for field in REQUIRED_FIELDS:
        if field not in chunk or chunk[field] in [None, ""]:
            errors.append(f"Line {line_number}: Missing required field: {field}")

    chunk_text = chunk.get("chunk_text", "")
    word_count = len(chunk_text.split())

    if word_count < MIN_CHUNK_WORDS:
        errors.append(f"Line {line_number}: Chunk is too short ({word_count} words).")

    if word_count > MAX_CHUNK_WORDS:
        errors.append(f"Line {line_number}: Chunk is too long ({word_count} words).")

    release_relevance = chunk.get("release_relevance")
    if release_relevance and release_relevance not in ALLOWED_RELEASE_RELEVANCE:
        errors.append(f"Line {line_number}: Invalid release_relevance '{release_relevance}'.")

    status = chunk.get("status")
    if status and status not in ALLOWED_STATUS:
        errors.append(f"Line {line_number}: Invalid status '{status}'.")

    if chunk.get("status") == "deprecated":
        errors.append(f"Line {line_number}: Deprecated chunk should not be indexed.")

    if chunk.get("release_relevance") == "deprecated":
        errors.append(
            f"Line {line_number}: Deprecated release relevance should not be indexed."
        )

    return errors


def main():
    if not CHUNKS_FILE.exists():
        print(f"Chunk file not found: {CHUNKS_FILE}")
        return 1

    all_errors = []
    chunk_count = 0

    with CHUNKS_FILE.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if not line:
                continue

            try:
                chunk = json.loads(line)
            except json.JSONDecodeError as error:
                all_errors.append(f"Line {line_number}: Invalid JSON: {error}")
                continue

            chunk_count += 1
            all_errors.extend(validate_chunk(chunk, line_number))

    if all_errors:
        print("\n❌ Chunk validation failed.")
        for error in all_errors:
            print(f"   - {error}")
        return 1

    print(f"✅ All {chunk_count} chunks passed validation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())