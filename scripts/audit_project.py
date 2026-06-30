from pathlib import Path
import sys
import yaml
import frontmatter

PROJECT_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_DIRS = [
    "data",
    "data/raw",
    "data/raw/drafts",
    "data/cleaned",
    "data/chunks",
    "data/metadata",
    "evals",
    "prompts",
    "schemas",
    "scripts",
    "templates",
]

REQUIRED_FILES = [
    "data/metadata/source_manifest.yaml",
    "data/metadata/exam_domain_map.yaml",
    "data/cleaned/agentforce-specialist-exam-guide.md",
    "evals/retrieval_tests.jsonl",
    "evals/refusal_tests.jsonl",
    "evals/answer_tests.jsonl",
    "scripts/run_pipeline.py",
    "scripts/validate_source_manifest.py",
    "scripts/validate_grounding_docs.py",
    "scripts/chunk_grounding_docs.py",
    "scripts/validate_chunks.py",
    "scripts/validate_evals.py",
    "scripts/test_keyword_retrieval.py",
    "scripts/test_refusal_behavior.py",
    "scripts/test_answer_quality.py",
]

CONFUSING_FILES = [
    "data/metadata/source-manifest.yaml",
    "data/metadata/source manifest.yaml",
    "source_manifest.yaml",
    "source-manifest.yaml",
]

GENERATED_OR_CACHE_PATTERNS = [
    "__pycache__",
    ".DS_Store",
    ".pytest_cache",
]

IGNORED_AUDIT_DIRS = {
    ".git",
    ".venv",
    "node_modules",
}

ALLOWED_CLEANED_STATUSES = {"active", "draft", "needs_review"}
PREFERRED_CLEANED_STATUSES = {"active", "needs_review"}


def check_required_dirs(errors):
    for relative_path in REQUIRED_DIRS:
        path = PROJECT_ROOT / relative_path
        if not path.exists():
            errors.append(f"Missing required directory: {relative_path}")
        elif not path.is_dir():
            errors.append(f"Expected directory but found file: {relative_path}")


def check_required_files(errors):
    for relative_path in REQUIRED_FILES:
        path = PROJECT_ROOT / relative_path
        if not path.exists():
            errors.append(f"Missing required file: {relative_path}")
        elif not path.is_file():
            errors.append(f"Expected file but found directory: {relative_path}")


def check_confusing_files(warnings):
    for relative_path in CONFUSING_FILES:
        path = PROJECT_ROOT / relative_path
        if path.exists():
            warnings.append(f"Confusing duplicate or misplaced file exists: {relative_path}")


def is_in_ignored_dir(path: Path):
    relative_parts = path.relative_to(PROJECT_ROOT).parts
    return any(part in IGNORED_AUDIT_DIRS for part in relative_parts)


def check_cache_files(warnings):
    for pattern in GENERATED_OR_CACHE_PATTERNS:
        for path in PROJECT_ROOT.rglob(pattern):
            if is_in_ignored_dir(path):
                continue

            relative_path = path.relative_to(PROJECT_ROOT)
            warnings.append(f"Generated/cache file or folder found: {relative_path}")


def load_manifest(errors):
    manifest_path = PROJECT_ROOT / "data" / "metadata" / "source_manifest.yaml"

    if not manifest_path.exists():
        errors.append("Cannot load manifest because source_manifest.yaml is missing.")
        return []

    try:
        data = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    except Exception as error:
        errors.append(f"Could not parse source_manifest.yaml: {error}")
        return []

    sources = data.get("sources") if isinstance(data, dict) else None

    if not isinstance(sources, list):
        errors.append("source_manifest.yaml must contain a top-level 'sources' list.")
        return []

    return sources


def check_manifest_ids(sources, errors, warnings):
    ids = []
    for source in sources:
        source_id = source.get("id") if isinstance(source, dict) else None

        if not source_id:
            errors.append("Manifest source missing id.")
            continue

        ids.append(source_id)

        if "_" in source_id:
            warnings.append(
                f"Manifest id uses underscore: {source_id}. Prefer hyphenated IDs for source ids."
            )

        if source.get("status") == "pending":
            warnings.append(
                f"Manifest source is still pending: {source_id}. Use active/draft/needs_review when ready."
            )

        if not source.get("source_url"):
            errors.append(f"Manifest source missing source_url: {source_id}")

    duplicate_ids = sorted({source_id for source_id in ids if ids.count(source_id) > 1})
    for source_id in duplicate_ids:
        errors.append(f"Duplicate manifest source id: {source_id}")


def check_cleaned_docs_against_manifest(sources, errors, warnings):
    manifest_ids = {
        source.get("id")
        for source in sources
        if isinstance(source, dict) and source.get("id")
    }

    cleaned_dir = PROJECT_ROOT / "data" / "cleaned"
    cleaned_files = sorted(cleaned_dir.glob("*.md"))

    if not cleaned_files:
        errors.append("No cleaned Markdown files found in data/cleaned.")
        return

    cleaned_ids = set()

    for path in cleaned_files:
        relative_path = path.relative_to(PROJECT_ROOT)

        try:
            doc = frontmatter.loads(path.read_text(encoding="utf-8"))
        except Exception as error:
            errors.append(f"{relative_path}: Could not parse frontmatter: {error}")
            continue

        doc_id = doc.metadata.get("id")
        status = doc.metadata.get("status")

        if not doc_id:
            errors.append(f"{relative_path}: Missing frontmatter id.")
            continue

        cleaned_ids.add(doc_id)

        if doc_id not in manifest_ids:
            errors.append(f"{relative_path}: id '{doc_id}' not found in source_manifest.yaml.")

        if status not in ALLOWED_CLEANED_STATUSES:
            errors.append(
                f"{relative_path}: status '{status}' is not allowed for cleaned docs."
            )

        if status == "draft":
            warnings.append(
                f"{relative_path}: status is draft. This is okay temporarily, but avoid indexing draft sources."
            )

        body = doc.content.strip()
        if len(body.split()) < 40:
            warnings.append(f"{relative_path}: body looks short. Confirm it has real source content.")

    manifest_ids_missing_docs = sorted(manifest_ids - cleaned_ids)

    for source_id in manifest_ids_missing_docs:
        warnings.append(
            f"Manifest source has no matching cleaned Markdown file yet: {source_id}"
        )


def check_drafts_not_in_cleaned(warnings):
    cleaned_dir = PROJECT_ROOT / "data" / "cleaned"

    for path in cleaned_dir.glob("*.md"):
        text = path.read_text(encoding="utf-8").lower()

        if (
            "paste the cleaned" in text
            or "paste official" in text
            or "placeholder text" in text
            or "placeholder here" in text
            or "insert placeholder" in text
        ):
            warnings.append(
                f"{path.relative_to(PROJECT_ROOT)} appears to contain placeholder text."
            )


def print_results(errors, warnings):
    if warnings:
        print("\n⚠️ Warnings")
        for warning in warnings:
            print(f"   - {warning}")

    if errors:
        print("\n❌ Project audit failed.")
        for error in errors:
            print(f"   - {error}")
        return 1

    print("\n✅ Project audit passed.")
    if not warnings:
        print("No warnings found.")
    return 0


def main():
    errors = []
    warnings = []

    check_required_dirs(errors)
    check_required_files(errors)
    check_confusing_files(warnings)
    check_cache_files(warnings)

    sources = load_manifest(errors)

    if sources:
        check_manifest_ids(sources, errors, warnings)
        check_cleaned_docs_against_manifest(sources, errors, warnings)

    check_drafts_not_in_cleaned(warnings)

    print(f"Project root: {PROJECT_ROOT}")
    print(f"Checked required dirs: {len(REQUIRED_DIRS)}")
    print(f"Checked required files: {len(REQUIRED_FILES)}")

    return print_results(errors, warnings)


if __name__ == "__main__":
    sys.exit(main())
