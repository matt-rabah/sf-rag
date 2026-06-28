from pathlib import Path
import subprocess
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

STEPS = [
    ("Validate source manifest", "scripts/validate_source_manifest.py"),
    ("Validate grounding documents", "scripts/validate_grounding_docs.py"),
    ("Chunk grounding documents", "scripts/chunk_grounding_docs.py"),
    ("Validate chunks", "scripts/validate_chunks.py"),
    ("Validate evals", "scripts/validate_evals.py"),
    ("Test keyword retrieval", "scripts/test_keyword_retrieval.py"),
    ("Test refusal behavior", "scripts/test_refusal_behavior.py"),
]


def run_step(label: str, script_path: str):
    print(f"\n=== {label} ===")

    result = subprocess.run(
        [sys.executable, script_path],
        cwd=PROJECT_ROOT,
        text=True,
    )

    if result.returncode != 0:
        print(f"\n❌ Pipeline stopped at: {label}")
        return result.returncode

    print(f"✅ Completed: {label}")
    return 0


def main():
    for label, script_path in STEPS:
        exit_code = run_step(label, script_path)

        if exit_code != 0:
            return exit_code

    print("\n✅ Pipeline completed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())