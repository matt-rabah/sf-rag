from pathlib import Path
import subprocess
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

STEPS = [
    ("Audit project structure", ["scripts/audit_project.py"]),
    ("Validate source manifest", ["scripts/validate_source_manifest.py"]),
    ("Validate grounding documents", ["scripts/validate_grounding_docs.py"]),
    ("Chunk grounding documents", ["scripts/chunk_grounding_docs.py"]),
    ("Validate chunks", ["scripts/validate_chunks.py"]),
    ("Validate evals", ["scripts/validate_evals.py"]),
    ("Test keyword retrieval", ["scripts/test_keyword_retrieval.py"]),
    ("Test refusal behavior", ["scripts/test_refusal_behavior.py"]),
    # Structural answer-quality checks (source-retrieved + answerable). Runs
    # without an API key; model accuracy is measured separately with a key via
    # `python3 scripts/test_answer_quality.py`.
    ("Answer-quality (structural)", ["scripts/test_answer_quality.py", "--no-model"]),
]


def run_step(label: str, argv: list):
    print(f"\n=== {label} ===")

    result = subprocess.run(
        [sys.executable, *argv],
        cwd=PROJECT_ROOT,
        text=True,
    )

    if result.returncode != 0:
        print(f"\n❌ Pipeline stopped at: {label}")
        return result.returncode

    print(f"✅ Completed: {label}")
    return 0


def main():
    for label, argv in STEPS:
        exit_code = run_step(label, argv)

        if exit_code != 0:
            return exit_code

    print("\n✅ Pipeline completed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())