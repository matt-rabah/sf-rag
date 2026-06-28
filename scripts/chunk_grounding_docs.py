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
            current_lines = [line]
        else:
            current_lines.append(line)

    if current_lines:
        sections.append(
            {
                "heading": current_heading,
                "text": "\n".join(current_lines).strip(),
            }
        )

    return [section for section in sections if section["text"]]


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


def make_chunk_record(metadata: dict, chunk_index: int, heading: str, chunk_text: str):
    source_id = metadata["id"]

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
        "chunk_text": chunk_text,
        "token_estimate": estimate_tokens(chunk_text),
        "contains_steps": bool(re.search(r"(^|\n)\s*\d+\.", chunk_text)),
        "contains_definition": " is " in chunk_text.lower() or " refers to " in chunk_text.lower(),
        "contains_limitations": any(
            phrase in chunk_text.lower()
            for phrase in ["limitation", "limited to", "does not", "cannot", "only"]
        ),
        "contains_exam_relevance": "exam relevance" in chunk_text.lower(),
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

        for section in sections:
            section_chunks = split_large_section(section["text"])

            for chunk_text in section_chunks:
                record = make_chunk_record(
                    metadata=metadata,
                    chunk_index=chunk_index,
                    heading=section["heading"],
                    chunk_text=chunk_text,
                )

                all_chunks.append(record)
                chunk_index += 1

        print(f"✅ Chunked {path.relative_to(PROJECT_ROOT)} into {chunk_index - 1} chunks")

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        for chunk in all_chunks:
            file.write(json.dumps(chunk, ensure_ascii=False) + "\n")

    print(f"\nWrote {len(all_chunks)} chunks to {OUTPUT_FILE.relative_to(PROJECT_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
