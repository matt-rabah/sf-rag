from pathlib import Path
import json
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
EVALS_DIR = PROJECT_ROOT / "evals"

REQUIRED_FIELDS = [
    "id",
    "certification",
    "exam_domain",
    "question",
    "expected_source_id",
    "expected_heading_contains",
    "expected_answer_contains",
    "notes",
]


def validate_eval(record: dict, path: Path, line_number: int):
    errors = []

    for field in REQUIRED_FIELDS:
        if field not in record or record[field] in [None, ""]:
            errors.append(f"{path.name} line {line_number}: Missing required field: {field}")

    expected_answer_contains = record.get("expected_answer_contains")
    if not isinstance(expected_answer_contains, list) or not expected_answer_contains:
        errors.append(
            f"{path.name} line {line_number}: expected_answer_contains must be a non-empty list."
        )

    return errors


def main():
    eval_files = sorted(EVALS_DIR.glob("*.jsonl"))

    if not eval_files:
        print(f"No eval files found in {EVALS_DIR}")
        return 1

    all_errors = []
    record_count = 0

    for path in eval_files:
        with path.open("r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()

                if not line:
                    continue

                try:
                    record = json.loads(line)
                except json.JSONDecodeError as error:
                    all_errors.append(f"{path.name} line {line_number}: Invalid JSON: {error}")
                    continue

                record_count += 1
                all_errors.extend(validate_eval(record, path, line_number))

    if all_errors:
        print("\n❌ Eval validation failed.")
        for error in all_errors:
            print(f"   - {error}")
        return 1

    print(f"✅ All {record_count} eval records passed validation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())