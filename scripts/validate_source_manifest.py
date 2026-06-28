from pathlib import Path
import re
import sys
import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLEANED_DIR = PROJECT_ROOT / "data" / "cleaned"
SOURCE_MANIFEST = PROJECT_ROOT / "data" / "metadata" / "source_manifest.yaml"

REQUIRED_MANIFEST_FIELDS = [
    "id",
    "title",
    "source_type",
    "source_url",
    "certification",
    "exam_domain",
    "product_area",
    "topic",
    "priority",
    "status",
    "retrieved_date",
    "release_relevance",
    "authority",
]


def parse_frontmatter(path: Path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)

    if not match:
        raise ValueError(f"{path.name}: Missing YAML frontmatter.")

    return yaml.safe_load(match.group(1)) or {}


def load_manifest():
    if not SOURCE_MANIFEST.exists():
        raise FileNotFoundError(f"Missing source manifest: {SOURCE_MANIFEST}")

    data = yaml.safe_load(SOURCE_MANIFEST.read_text(encoding="utf-8")) or {}
    sources = data.get("sources", [])

    if not isinstance(sources, list):
        raise ValueError("source_manifest.yaml must contain a top-level 'sources' list.")

    return sources


def validate_manifest_source(source: dict, index: int):
    errors = []

    for field in REQUIRED_MANIFEST_FIELDS:
        if field not in source or source[field] in [None, ""]:
            errors.append(f"Manifest source #{index}: Missing required field: {field}")

    return errors


def main():
    errors = []

    try:
        sources = load_manifest()
    except Exception as error:
        print(f"❌ {error}")
        return 1

    manifest_ids = set()

    for index, source in enumerate(sources, start=1):
        source_errors = validate_manifest_source(source, index)
        errors.extend(source_errors)

        source_id = source.get("id")
        if source_id:
            if source_id in manifest_ids:
                errors.append(f"Duplicate source id in manifest: {source_id}")
            manifest_ids.add(source_id)

    markdown_files = sorted(CLEANED_DIR.glob("*.md"))

    if not markdown_files:
        errors.append(f"No cleaned Markdown files found in {CLEANED_DIR}")

    for path in markdown_files:
        try:
            frontmatter = parse_frontmatter(path)
        except ValueError as error:
            errors.append(str(error))
            continue

        doc_id = frontmatter.get("id")

        if not doc_id:
            errors.append(f"{path.name}: Missing frontmatter id.")
            continue

        if doc_id not in manifest_ids:
            errors.append(
                f"{path.relative_to(PROJECT_ROOT)} has id '{doc_id}' "
                f"but no matching entry in source_manifest.yaml."
            )

    if errors:
        print("\n❌ Source manifest validation failed.")
        for error in errors:
            print(f"   - {error}")
        return 1

    print(f"✅ Source manifest passed validation.")
    print(f"Validated {len(sources)} manifest sources and {len(markdown_files)} cleaned documents.")
    return 0


if __name__ == "__main__":
    sys.exit(main())