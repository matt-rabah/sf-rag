"""Build the optional semantic retrieval index from the chunked corpus.

Run this once (and after re-chunking) to enable hybrid retrieval in
scripts/answer_question.py. Requires the extra dependencies in requirements.txt
(scikit-learn, numpy, joblib). If the index is absent, the answerer falls back to
keyword-only retrieval automatically.

    python3 scripts/build_embeddings.py
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_keyword_retrieval import load_jsonl  # noqa: E402
import semantic_index  # noqa: E402

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHUNKS_FILE = PROJECT_ROOT / "data" / "chunks" / "grounding_chunks.jsonl"


def main() -> int:
    try:
        import sklearn  # noqa: F401
    except ImportError:
        print(
            "❌ scikit-learn is not installed. Install the optional deps with:\n"
            "    python3 -m pip install -r requirements.txt"
        )
        return 1

    chunks = load_jsonl(CHUNKS_FILE)
    if not chunks:
        print("❌ No chunks found. Run scripts/chunk_grounding_docs.py first.")
        return 1

    index = semantic_index.build(chunks)
    print(
        f"✅ Built semantic index for {len(index.chunk_ids)} chunks "
        f"({index.embeddings.shape[1]} dims) -> {semantic_index.ARTIFACT.relative_to(PROJECT_ROOT)}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
