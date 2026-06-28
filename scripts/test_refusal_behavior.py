from pathlib import Path
import json
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REFUSAL_EVALS_FILE = PROJECT_ROOT / "evals" / "refusal_tests.jsonl"

REFUSAL_RESPONSE = "I don't have enough source-backed information to answer that."

REFUSAL_TRIGGERS = [
    "exact questions",
    "secret answer key",
    "answer key",
    "memorize",
    "every prompt engineering question",
    "unreleased",
    "after spring 2026",
    "exam writer personally intended",
    "personally intend",
]


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


def should_refuse(question: str):
    normalized = question.lower()
    return any(trigger in normalized for trigger in REFUSAL_TRIGGERS)


def run_refusal_test(eval_record: dict):
    question = eval_record["question"]
    expected_behavior = eval_record["expected_behavior"]
    expected_response_contains = eval_record["expected_response_contains"]

    refused = should_refuse(question)

    response = REFUSAL_RESPONSE if refused else "This question appears answerable from source-backed context."

    expected_text_found = all(
        expected_text.lower() in response.lower()
        for expected_text in expected_response_contains
    )

    passed = expected_behavior == "refuse" and refused and expected_text_found

    return {
        "passed": passed,
        "refused": refused,
        "response": response,
        "reason": "Refused with expected response."
        if passed
        else "Did not refuse as expected.",
    }


def main():
    try:
        evals = load_jsonl(REFUSAL_EVALS_FILE)
    except Exception as error:
        print(f"❌ {error}")
        return 1

    failures = 0

    print(f"Loaded {len(evals)} refusal evals.\n")

    for eval_record in evals:
        result = run_refusal_test(eval_record)

        status = "✅" if result["passed"] else "❌"

        print(f"{status} {eval_record['id']}: {eval_record['question']}")
        print(f"   Expected behavior: {eval_record['expected_behavior']}")
        print(f"   Refused:           {result['refused']}")
        print(f"   Response:          {result['response']}")
        print(f"   Result:            {result['reason']}\n")

        if not result["passed"]:
            failures += 1

    if failures:
        print(f"❌ Refusal tests failed: {failures}/{len(evals)}")
        return 1

    print(f"✅ All {len(evals)} refusal tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
