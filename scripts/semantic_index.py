"""Optional semantic (dense-ish) retrieval backend for SF-RAG.

This adds a semantic similarity signal to complement the keyword retriever, so
paraphrased practice questions (which share meaning but not exact words) still
retrieve the right grounding chunks.

Default backend: TF-IDF + Truncated SVD (latent semantic analysis). It is
download-free (pure scikit-learn, no model weights to fetch), deterministic, and
runs anywhere PyPI is reachable. It captures co-occurrence/latent structure
beyond raw keyword overlap. For stronger synonym/paraphrase matching you can swap
in dense transformer embeddings later (see embed_texts / embed_query below) in an
environment that allows model downloads — the rest of the retrieval code is
agnostic to which backend produced the vectors.

Everything here is optional: if scikit-learn or the built index is missing,
load() returns None and the retriever falls back to keyword-only scoring with no
change in behavior. Build the index with: python3 scripts/build_embeddings.py
"""

from pathlib import Path
import json

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = PROJECT_ROOT / "data" / "chunks" / "semantic_index.joblib"

N_COMPONENTS = 200  # SVD latent dimensions (capped to corpus size at build time)


def chunk_embed_text(chunk: dict) -> str:
    """The text used to represent a chunk in the semantic space.

    Mirrors the fields the keyword retriever scores against, so both signals see
    the same content.
    """
    return " ".join(
        str(chunk.get(field, ""))
        for field in ("title", "exam_domain", "product_area", "topic", "chunk_heading", "chunk_text")
    )


def build(chunks: list) -> "SemanticIndex":
    """Fit the LSA pipeline over the chunks and persist it to ARTIFACT."""
    import numpy as np
    import joblib
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.decomposition import TruncatedSVD
    from sklearn.preprocessing import normalize

    chunk_ids = [c["chunk_id"] for c in chunks]
    texts = [chunk_embed_text(c) for c in chunks]

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2), sublinear_tf=True, stop_words="english", min_df=1
    )
    tfidf = vectorizer.fit_transform(texts)

    # SVD components must be < min(n_samples, n_features).
    n_components = min(N_COMPONENTS, tfidf.shape[0] - 1, tfidf.shape[1] - 1)
    svd = TruncatedSVD(n_components=n_components, random_state=0)
    reduced = svd.fit_transform(tfidf)
    embeddings = normalize(reduced).astype("float32")

    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {"chunk_ids": chunk_ids, "embeddings": embeddings, "vectorizer": vectorizer, "svd": svd},
        ARTIFACT,
    )
    return SemanticIndex(chunk_ids, embeddings, vectorizer, svd)


class SemanticIndex:
    def __init__(self, chunk_ids, embeddings, vectorizer, svd):
        self.chunk_ids = chunk_ids
        self.embeddings = embeddings
        self.vectorizer = vectorizer
        self.svd = svd

    def scores(self, query: str) -> dict:
        """Return {chunk_id: cosine_similarity} for the query (cosine in [-1, 1])."""
        from sklearn.preprocessing import normalize

        q = normalize(self.svd.transform(self.vectorizer.transform([query]))).astype("float32")
        sims = (self.embeddings @ q[0])
        return {cid: float(s) for cid, s in zip(self.chunk_ids, sims)}


def load():
    """Load the persisted index, or return None if unavailable (keyword-only fallback)."""
    if not ARTIFACT.exists():
        return None
    try:
        import joblib

        data = joblib.load(ARTIFACT)
        return SemanticIndex(
            data["chunk_ids"], data["embeddings"], data["vectorizer"], data["svd"]
        )
    except Exception:
        return None
