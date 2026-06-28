from pathlib import Path
import json
import re
import sys
import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLEANED_DIR = PROJECT_ROOT / "data" / "cleaned"
CHUNKS_DIR = PROJECT_ROOT / "data" / "chunks"
OUTPUT_FILE = CHUNKS_DIR / "grounding_chunks.jsonl"

REQUIRED_FIELDS = [
    "id",
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
]

MAX_WORDS_PER_CHUNK = 350
MIN_WORDS_PER_CHUNK = 20

PLACEHOLDER_PHRASES = [
    "write a short summary",
    "paste or clean the source content here",
    "explain why this content matters",
    "add any implementation notes",
    "concept 1",
    "concept 2",
    "concept 3",
    "example source title",
]


def parse_markdown_with_frontmatter(path: Path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)

    if not match:
        raise ValueError(f"{path.name}: Missing YAML frontmatter.")

    metadata = yaml.safe_load(match.group(1)) or {}
    body = match.group(2).strip()

    missing = [field for field in REQUIRED_FIELDS if not metadata.get(field)]
    if missing:
        raise ValueError(f"{path.name}: Missing required fields: {', '.join(missing)}")

    if not body:
        raise ValueError(f"{path.name}: Document body is empty.")

    return metadata, body


def split_by_headings(markdown_body: str):
    sections = []
    current_heading = "Document"
    current_lines = []

    for line in markdown_body.splitlines():
        heading_match = re.match(r"^(#{1,6})\s+(.*)", line)

        if heading_match:
            if current_lines:
                sections.append(
                    {
                        "heading": current_heading,
                        "text": "\n".join(current_lines).strip(),
                    }
                )

            current_heading = heading_match.group(2).strip()
            current_lines = []
        else:
            current_lines.append(line)

    if current_lines:
        sections.append(
            {
                "heading": current_heading,
                "text": "\n".join(current_lines).strip(),
            }
        )

    return [section for section in sections if section["text"].strip()]


def split_large_section(section_text: str, max_words: int = MAX_WORDS_PER_CHUNK):
    words = section_text.split()

    if len(words) <= max_words:
        return [section_text]

    chunks = []
    for index in range(0, len(words), max_words):
        chunks.append(" ".join(words[index : index + max_words]))

    return chunks


def estimate_tokens(text: str):
    # Rough estimate: 1 token ≈ 0.75 words, so tokens ≈ words / 0.75.
    return round(len(text.split()) / 0.75)


def is_placeholder_or_too_short(text: str):
    normalized = text.lower().strip()
    word_count = len(normalized.split())

    if word_count < MIN_WORDS_PER_CHUNK:
        return True

    return any(phrase in normalized for phrase in PLACEHOLDER_PHRASES)


def make_chunk_record(metadata: dict, chunk_index: int, heading: str, chunk_text: str):
    source_id = metadata["id"]

    full_chunk_text = f"{heading}\n\n{chunk_text}".strip()

    return {
        "chunk_id": f"{source_id}__{chunk_index:03d}",
        "source_id": source_id,
        "title": metadata["title"],
        "source_type": metadata["source_type"],
        "source_url": metadata["source_url"],
        "certification": metadata["certification"],
        "exam_domain": metadata["exam_domain"],
        "product_area": metadata["product_area"],
        "topic": metadata["topic"],
        "retrieved_date": str(metadata["retrieved_date"]),
        "release_relevance": metadata["release_relevance"],
        "authority": metadata["authority"],
        "status": metadata["status"],
        "chunk_index": chunk_index,
        "chunk_heading": heading,
        "chunk_text": full_chunk_text,
        "token_estimate": estimate_tokens(full_chunk_text),
        "contains_steps": bool(re.search(r"(^|\n)\s*\d+\.", full_chunk_text)),
        "contains_definition": " is " in full_chunk_text.lower()
        or " refers to " in full_chunk_text.lower(),
        "contains_limitations": any(
            phrase in full_chunk_text.lower()
            for phrase in ["limitation", "limited to", "does not", "cannot", "only"]
        ),
        "contains_exam_relevance": "exam relevance" in full_chunk_text.lower(),
    }


def main():
    CHUNKS_DIR.mkdir(parents=True, exist_ok=True)

    markdown_files = sorted(CLEANED_DIR.glob("*.md"))

    if not markdown_files:
        print(f"No Markdown files found in {CLEANED_DIR}")
        return 1

    all_chunks = []

    for path in markdown_files:
        metadata, body = parse_markdown_with_frontmatter(path)
        sections = split_by_headings(body)

        chunk_index = 1
        skipped_count = 0

        for section in sections:
            section_chunks = split_large_section(section["text"])

            for chunk_text in section_chunks:
                if is_placeholder_or_too_short(chunk_text):
                    skipped_count += 1
                    continue

                record = make_chunk_record(
                    metadata=metadata,
                    chunk_index=chunk_index,
                    heading=section["heading"],
                    chunk_text=chunk_text,
                )

                all_chunks.append(record)
                chunk_index += 1

        print(
            f"✅ Chunked {path.relative_to(PROJECT_ROOT)} into "
            f"{chunk_index - 1} chunks; skipped {skipped_count}"
        )

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        for chunk in all_chunks:
            file.write(json.dumps(chunk, ensure_ascii=False) + "\n")

    print(f"\nWrote {len(all_chunks)} chunks to {OUTPUT_FILE.relative_to(PROJECT_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
