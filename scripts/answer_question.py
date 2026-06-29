"""Answer a Salesforce certification practice question from a screenshot or text.

This is the source-grounded answering entrypoint for the SF-RAG project. It lets
you point at a photo/screenshot of a practice question instead of copying and
pasting the text, then produces a grounded, source-cited explanation.

Pipeline:
  1. Read the question. From an image, Claude (vision) extracts the question and
     answer options. From --text, the text is used directly.
  2. Retrieve. The extracted question runs through the existing keyword retriever
     (scripts/test_keyword_retrieval.py) to pull the top grounding chunks.
  3. Answer. Claude answers using one of the prompt templates in prompts/, with
     {{retrieved_context}} filled from the retrieved chunks. The model is
     instructed to answer only from retrieved context and to refuse when the
     context is insufficient (see prompts/ and sf-rag-guidelines.md).

Grounding and hallucination control live in the prompt templates, not here. This
script only wires retrieval to the model.

Requires the ANTHROPIC_API_KEY environment variable for any step that calls the
model. Use --show-context (with --text) to inspect retrieval without a model call.

Examples:
  python3 scripts/answer_question.py --image ~/Desktop/q12.png
  python3 scripts/answer_question.py --text "Which retriever type ..." --prompt technical
  python3 scripts/answer_question.py --text "What does SOMA mean?" --show-context
"""

from pathlib import Path
import argparse
import base64
import sys

# Reuse the project's existing retrieval logic so the answering path scores
# chunks exactly the way the retrieval evals do.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_keyword_retrieval import load_jsonl, score_chunk  # noqa: E402

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHUNKS_FILE = PROJECT_ROOT / "data" / "chunks" / "grounding_chunks.jsonl"
PROMPTS_DIR = PROJECT_ROOT / "prompts"

MODEL = "claude-opus-4-8"
DEFAULT_TOP_K = 6

# Friendly prompt names mapped to the templates in prompts/.
PROMPT_TEMPLATES = {
    "scenario": "scenario_based_image_prompt.md",
    "grounding": "data_grounding_rag_image_prompt.md",
    "technical": "technical_config_image_prompt.md",
}

IMAGE_MEDIA_TYPES = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
}

EXTRACTION_INSTRUCTION = (
    "This image is a single multiple-choice certification practice question. "
    "Transcribe it exactly as plain text: the full question stem followed by "
    "every answer option with its letter (A, B, C, ...). Do not answer it, "
    "explain it, or add commentary. Output only the transcribed question and "
    "options."
)


def media_type_for(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix not in IMAGE_MEDIA_TYPES:
        raise SystemExit(
            f"Unsupported image type '{suffix}'. Use one of: "
            f"{', '.join(sorted(IMAGE_MEDIA_TYPES))}."
        )
    return IMAGE_MEDIA_TYPES[suffix]


def load_image_block(path: Path) -> dict:
    data = base64.standard_b64encode(path.read_bytes()).decode("utf-8")
    return {
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": media_type_for(path),
            "data": data,
        },
    }


def make_client():
    try:
        import anthropic
    except ImportError:
        raise SystemExit(
            "The 'anthropic' package is required. Install it with:\n"
            "    python3 -m pip install -r requirements.txt"
        )
    import os

    if not (os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN")):
        raise SystemExit(
            "Set ANTHROPIC_API_KEY (or ANTHROPIC_AUTH_TOKEN) to call the model. "
            "To preview retrieval only, use --text with --show-context."
        )
    return anthropic.Anthropic()


def message_text(response) -> str:
    return "".join(block.text for block in response.content if block.type == "text").strip()


def extract_question_from_image(client, image_block: dict) -> str:
    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [image_block, {"type": "text", "text": EXTRACTION_INSTRUCTION}],
            }
        ],
    )
    text = message_text(response)
    if not text:
        raise SystemExit("Could not read a question from the image.")
    return text


def retrieve(question: str, chunks: list, top_k: int) -> list:
    scored = sorted(
        ({"score": score_chunk(question, chunk), "chunk": chunk} for chunk in chunks),
        key=lambda item: item["score"],
        reverse=True,
    )
    return scored[:top_k]


def build_retrieved_context(results: list) -> str:
    blocks = []
    for rank, result in enumerate(results, 1):
        chunk = result["chunk"]
        blocks.append(
            f"[Source {rank}] {chunk.get('title', '')}\n"
            f"Exam domain: {chunk.get('exam_domain', '')} | Topic: {chunk.get('topic', '')}\n"
            f"Source URL: {chunk.get('source_url', '')}\n"
            f"Heading: {chunk.get('chunk_heading', '')}\n"
            f"{chunk.get('chunk_text', '')}"
        )
    return "\n\n---\n\n".join(blocks)


def load_prompt(name: str, retrieved_context: str) -> str:
    template = (PROMPTS_DIR / PROMPT_TEMPLATES[name]).read_text(encoding="utf-8")
    return template.replace("{{retrieved_context}}", retrieved_context)


def answer(client, prompt_text: str, image_block: dict | None) -> str:
    content = []
    if image_block is not None:
        content.append(image_block)
    content.append({"type": "text", "text": prompt_text})
    response = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        thinking={"type": "adaptive"},
        messages=[{"role": "user", "content": content}],
    )
    return message_text(response)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Answer a Salesforce cert practice question from a screenshot or text, "
        "grounded in the project corpus."
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--image", type=Path, help="Path to a screenshot/photo of the question.")
    source.add_argument("--text", help="Question text (use instead of an image).")
    parser.add_argument(
        "--prompt",
        choices=sorted(PROMPT_TEMPLATES),
        default="scenario",
        help="Answer prompt template to use (default: scenario).",
    )
    parser.add_argument(
        "--top-k", type=int, default=DEFAULT_TOP_K, help=f"Chunks to retrieve (default: {DEFAULT_TOP_K})."
    )
    parser.add_argument(
        "--show-context",
        action="store_true",
        help="Print the question and retrieved context, then stop (no answer generated).",
    )
    args = parser.parse_args()

    if args.image and not args.image.exists():
        raise SystemExit(f"Image not found: {args.image}")

    chunks = load_jsonl(CHUNKS_FILE)

    # An image always needs the model for extraction; text + --show-context does not.
    needs_model = bool(args.image) or not args.show_context
    client = make_client() if needs_model else None

    image_block = load_image_block(args.image) if args.image else None

    if args.image:
        print("Reading question from image...", file=sys.stderr)
        question = extract_question_from_image(client, image_block)
    else:
        question = args.text

    results = retrieve(question, chunks, args.top_k)
    retrieved_context = build_retrieved_context(results)

    if args.show_context:
        print("=== Extracted question ===")
        print(question)
        print("\n=== Retrieved context ===")
        print(retrieved_context)
        return 0

    prompt_text = load_prompt(args.prompt, retrieved_context)
    print("Answering from retrieved context...", file=sys.stderr)
    print(answer(client, prompt_text, image_block))
    return 0


if __name__ == "__main__":
    sys.exit(main())
