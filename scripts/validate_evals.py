from pathlib import Path
import json
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
EVALS_DIR = PROJECT_ROOT / "evals"

BASE_REQUIRED_FIELDS = [
    "id",
    "certification",
    "exam_domain",
    "question",
    "notes",
]

RETRIEVAL_REQUIRED_FIELDS = [
    "expected_source_id",
    "expected_heading_contains",
    "expected_answer_contains",
]

REFUSAL_REQUIRED_FIELDS = [
    "expected_behavior",
    "expected_response_contains",
]


def validate_list_field(record: dict, field: str, path: Path, line_number: int):
    value = record.get(field)

    if not isinstance(value, list) or not value:
        return [f"{path.name} line {line_number}: {field} must be a non-empty list."]

    return []


def validate_eval(record: dict, path: Path, line_number: int):
    errors = []

    for field in BASE_REQUIRED_FIELDS:
        if field not in record or record[field] in [None, ""]:
            errors.append(f"{path.name} line {line_number}: Missing required field: {field}")

    is_refusal_eval = record.get("expected_behavior") == "refuse"

    if is_refusal_eval:
        for field in REFUSAL_REQUIRED_FIELDS:
            if field not in record or record[field] in [None, ""]:
                errors.append(f"{path.name} line {line_number}: Missing required field: {field}")

        errors.extend(validate_list_field(record, "expected_response_contains", path, line_number))

        if record.get("expected_behavior") != "refuse":
            errors.append(
                f"{path.name} line {line_number}: expected_behavior must be 'refuse' for refusal evals."
            )

    else:
        for field in RETRIEVAL_REQUIRED_FIELDS:
            if field not in record or record[field] in [None, ""]:
                errors.append(f"{path.name} line {line_number}: Missing required field: {field}")

        errors.extend(validate_list_field(record, "expected_heading_contains", path, line_number))
        errors.extend(validate_list_field(record, "expected_answer_contains", path, line_number))

    return errors


def main():
    eval_files = sorted(EVALS_DIR.glob("*.jsonl"))

    if not eval_files:
        print(f"No eval files found in {EVALS_DIR}")
        return 1

    all_errors = []
    record_count = 0
    seen_eval_ids = {}

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

                eval_id = record.get("id")
                if eval_id:
                    if eval_id in seen_eval_ids:
                        first_path, first_line = seen_eval_ids[eval_id]
                        all_errors.append(
                            f"{path.name} line {line_number}: Duplicate eval id '{eval_id}' also found in {first_path} line {first_line}."
                        )
                    else:
                        seen_eval_ids[eval_id] = (path.name, line_number)

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