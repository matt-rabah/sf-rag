from pathlib import Path
import sys
import re
import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLEANED_DIR = PROJECT_ROOT / "data" / "cleaned"

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

ALLOWED_SOURCE_TYPES = {
    "salesforce_help",
    "trailhead",
    "exam_guide",
    "release_notes",
    "developer_docs",
    "personal_notes",
    "practice_question",
}

ALLOWED_RELEASE_RELEVANCE = {
    "current",
    "needs_review",
    "archived",
    "deprecated",
}

ALLOWED_AUTHORITY = {
    "official",
    "salesforce",
    "personal",
    "third_party",
}

ALLOWED_STATUS = {
    "active",
    "draft",
    "needs_review",
    "deprecated",
}


def parse_markdown_with_frontmatter(path: Path):
    text = path.read_text(encoding="utf-8")

    match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)

    if not match:
        raise ValueError("Missing YAML frontmatter block at the top of the file.")

    frontmatter_raw = match.group(1)
    body = match.group(2).strip()

    try:
        metadata = yaml.safe_load(frontmatter_raw) or {}
    except yaml.YAMLError as error:
        raise ValueError(f"Invalid YAML frontmatter: {error}")

    return metadata, body


def validate_file(path: Path):
    errors = []

    try:
        metadata, body = parse_markdown_with_frontmatter(path)
    except ValueError as error:
        return [str(error)]

    for field in REQUIRED_FIELDS:
        if field not in metadata or metadata[field] in [None, ""]:
            errors.append(f"Missing required field: {field}")

    source_type = metadata.get("source_type")
    if source_type and source_type not in ALLOWED_SOURCE_TYPES:
        errors.append(
            f"Invalid source_type '{source_type}'. "
            f"Allowed values: {sorted(ALLOWED_SOURCE_TYPES)}"
        )

    release_relevance = metadata.get("release_relevance")
    if release_relevance and release_relevance not in ALLOWED_RELEASE_RELEVANCE:
        errors.append(
            f"Invalid release_relevance '{release_relevance}'. "
            f"Allowed values: {sorted(ALLOWED_RELEASE_RELEVANCE)}"
        )

    authority = metadata.get("authority")
    if authority and authority not in ALLOWED_AUTHORITY:
        errors.append(
            f"Invalid authority '{authority}'. "
            f"Allowed values: {sorted(ALLOWED_AUTHORITY)}"
        )

    status = metadata.get("status")
    if status and status not in ALLOWED_STATUS:
        errors.append(
            f"Invalid status '{status}'. " f"Allowed values: {sorted(ALLOWED_STATUS)}"
        )

    if not body:
        errors.append("Document body is empty.")

    if len(body.split()) < 50:
        errors.append("Document body is very short. Confirm this is intentional.")

    return errors


def main():
    markdown_files = sorted(CLEANED_DIR.glob("*.md"))

    if not markdown_files:
        print(f"No Markdown files found in {CLEANED_DIR}")
        return 1

    has_errors = False

    for path in markdown_files:
        errors = validate_file(path)

        if errors:
            has_errors = True
            print(f"\n❌ {path.relative_to(PROJECT_ROOT)}")
            for error in errors:
                print(f"   - {error}")
        else:
            print(f"✅ {path.relative_to(PROJECT_ROOT)}")

    if has_errors:
        print("\nValidation failed.")
        return 1

    print("\nAll grounding documents passed validation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
