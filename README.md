# SF-RAG

A Salesforce certification-prep RAG project focused on low-hallucination, source-backed answers.

The goal is to build a grounded study assistant that can answer Salesforce certification questions
using trusted source material, explain why answers are correct or incorrect, and refuse when the
retrieved context is insufficient.

## Project Goal

Build a retrieval-augmented generation system for Salesforce certification prep.

The system should:

- Ground answers in official or trusted Salesforce sources.
- Support certification-style Q&A.
- Explain multiple-choice answers clearly.
- Cite source material when available.
- Avoid unsupported answers and hallucinations.
- Keep source documents clean, validated, and easy to inspect.

This is not intended to be a broad Salesforce chatbot. It is a certification-focused RAG system.

## Current Scope

Initial focus:

- Salesforce Certified Agentforce Specialist
- Agentforce
- Data 360 / Data Cloud terminology where applicable
- Prompt Builder
- Agent Builder
- Agentforce Data Libraries
- Retrievers
- Search indexes
- Hybrid search
- Grounding
- Trust Layer
- Testing and deployment patterns

Additional certifications can be added later after the first corpus and evaluation workflow are
reliable.

## Project Structure

```text
sf-rag/
├─ data/
│  ├─ chunks/
│  ├─cleaned/
│  ├─metadata/
│  ├─raw/
├─ docs/
│  ├─ eval_tests/
│  ├─grounding_docs/
├─ evals/
├─ prompts/
├─ salesforce//
├─ schemas/
├─ scripts/
├─ templates/
├─ README.md
├─ requirements.txt
└─ sf-rag-guidelines.md
```

## Folder Purpose

### `data/raw/`

Original source material before cleaning.

Examples:

- Raw HTML
- Copied source text
- PDFs
- Screenshots
- Exported documents

Raw files should not be indexed directly.

### `data/cleaned/`

Clean Markdown files with YAML frontmatter.

These are the human-readable source documents used for grounding.

Every file in this folder must follow the grounding document template and pass validation before
chunking.

### `data/chunks/`

Chunked output files, usually JSONL.

Each line should represent one chunk ready for indexing.

### `data/metadata/`

Project metadata and source tracking.

Important file:

```text
data/metadata/source_manifest.yaml
```

This file tracks source IDs, URLs, source types, priorities, and ingestion status.

### `templates/`

Reusable templates for source documents, prompts, chunks, and evals.

Templates should not be indexed.

### `scripts/`

Python scripts for validation, cleaning, chunking, ingestion, and indexing.

### `prompts/`

Prompt templates for RAG answers, quiz explanations, refusal behavior, and evaluation.

### `evals/`

Evaluation test cases.

These should be used to test retrieval quality and answer quality.

### `schemas/`

Validation schemas for metadata, chunk records, and other structured files.

## Source Format

Grounding documents should use:

```text
Markdown + YAML frontmatter
```

Example:

```markdown
---
id: example-source-id
title: Example Source Title
source_type: salesforce_help
source_url: https://example.com/source-page
certification: Agentforce Specialist
exam_domain: Agentforce and Data 360
product_area: Agentforce
topic: Example Topic
retrieved_date: 2026-06-27
release_relevance: current
authority: official
status: active
---

# Example Source Title

## Summary

Short summary of the source.

## Source Content

Cleaned source content goes here.
```

## Required Frontmatter Fields

Every Markdown file in `data/cleaned/` must include:

- `id`
- `title`
- `source_type`
- `source_url`
- `certification`
- `exam_domain`
- `product_area`
- `topic`
- `retrieved_date`
- `release_relevance`
- `authority`
- `status`

Documents missing these fields should not be chunked or indexed.

## Recommended Source Priority

Prefer sources in this order:

1. Official Salesforce exam guides
2. Salesforce Help
3. Salesforce Developer documentation
4. Salesforce Trailhead
5. Salesforce release notes
6. Personal notes based on verified sources
7. Practice questions and corrected misses
8. Third-party sources, only when clearly labeled

Official Salesforce sources should override personal notes or third-party material.

## Setup

From the project root:

```bash
cd /Users/mattrabah/Desktop/sf-rag
python3 -m pip install -r requirements.txt
```

## Validate Grounding Documents

Run:

```bash
cd /Users/mattrabah/Desktop/sf-rag
python3 scripts/validate_grounding_docs.py
```

The validator checks files in:

```text
data/cleaned/
```

Templates are not validated because they are examples, not grounding documents.

## Intended Workflow

Use this workflow for adding source material:

1. Add the source to `data/metadata/source_manifest.yaml`.
2. Save raw source material in `data/raw/` if needed.
3. Create a cleaned Markdown file in `data/cleaned/`.
4. Add required YAML frontmatter.
5. Run the grounding document validator.
6. Fix validation errors.
7. Chunk the validated document into JSONL.
8. Index the chunks.
9. Test retrieval using eval questions.
10. Test answer generation only after retrieval works.

## Answer a Question from a Screenshot

You can answer a practice question from a photo or screenshot instead of copying
and pasting the text. The script reads the question from the image, retrieves
source-backed context from the corpus, and returns a grounded, cited explanation.

Set an API key first:

```bash
export ANTHROPIC_API_KEY=your-key
```

Then run:

```bash
# From a screenshot or phone photo of the question
python3 scripts/answer_question.py --image /path/to/question.png

# From text instead of an image
python3 scripts/answer_question.py --text "Which retriever type uses hybrid search?"

# Preview only what was retrieved, with no model call (no API key needed)
python3 scripts/answer_question.py --text "What does SOMA mean?" --show-context
```

Useful flags:

- `--prompt {scenario,grounding,technical}` selects the answer template in `prompts/`
  (default `scenario`).
- `--top-k N` sets how many grounding chunks to retrieve (default 6).

Supported image types: PNG, JPG/JPEG, GIF, WebP.

### Answer Format

Each answer is returned as the correct letter, a confidence score out of 10, and
a one-sentence reason each remaining option is wrong:

```text
Answer: C
Confidence: 8/10

Why the others are wrong:
- A: ...
- B: ...
- D: ...
```

Questions with an E option are handled the same way. When retrieval is too weak
to support an answer, the response is the refusal phrase instead (see below).

### Hallucination Controls

The answering script layers several safeguards on top of the prompt templates:

- **Relevance gate.** If the best retrieved chunk scores below the relevance
  threshold, the script refuses immediately (`I don't have enough source-backed
  information to answer that.`) without calling the model. Out-of-corpus
  questions can't produce an invented answer. Tune `MIN_TOP_SCORE` /
  `MIN_CHUNK_SCORE` in `scripts/answer_question.py`.
- **No padding with weak chunks.** Low-scoring chunks are dropped rather than
  used to fill the context, so the model can't latch onto a tangential source.
- **Grounding system prompt.** The model is told to answer only from the
  retrieved context, cite only URLs present in that context, and refuse when it
  is insufficient.
- **Neutral transcription.** The answer step sees a transcription of the
  question, never the raw screenshot — so a "correct" answer that is highlighted
  or pre-selected in a practice-app screenshot cannot leak in and bypass
  grounding.

Use `--show-context` to see retrieval scores and whether the gate would refuse.

### Faithfulness Verification

After the model answers, a **deterministic guard runs automatically** (no API key,
no flag) and appends a caution if it finds:

- a **URL or "Source N" reference** that is not in / exceeds the retrieved context
  (an invented citation), or
- a chosen answer whose terms are **largely absent from the retrieved context**
  (an answer grounded in nothing).

For a stronger check, add `--verify` to run a second **LLM entailment pass**: it
re-reads the retrieved context and confirms it actually supports the chosen
answer. If it does not, the answer is flagged so you don't trust an ungrounded
pick. (Lexical overlap alone can't tell a correct option from an in-vocabulary
distractor, so the entailment pass is the real support check; the deterministic
guard catches the obvious failures for free.)

## Hybrid Retrieval (optional)

By default the answerer retrieves with the keyword scorer. You can add a
**semantic** signal so paraphrased questions (same meaning, different words) rank
the right chunks higher:

```bash
python3 -m pip install -r requirements.txt   # installs scikit-learn, numpy, joblib
python3 scripts/build_embeddings.py          # builds data/chunks/semantic_index.joblib
```

Once the index exists, `answer_question.py` automatically runs in **hybrid** mode
(keyword + semantic, blended with reciprocal rank fusion). If the index or the
optional dependencies are missing, it falls back to keyword-only with no change in
behavior. Rebuild the index after re-chunking.

**Safety note:** the semantic backend (TF-IDF + SVD / LSA) is download-free and
deterministic, but on a small corpus it does *not* reliably tell an off-topic
question from an on-topic one. So semantics only **re-rank** chunks that already
passed the keyword relevance gate — the decision of *whether to answer at all*
stays keyword-only. This keeps out-of-corpus questions refusing correctly. The
embedding backend is pluggable (`scripts/semantic_index.py`): in an environment
that allows model downloads, a dense transformer embedder can be swapped in for
stronger paraphrase matching.

## Measuring Answer Quality

`evals/answer_tests.jsonl` is a labeled set of multiple-choice questions (with
known correct answers, each grounded in a specific source document). The scorer
runs them through the same retrieval + gate + answer path as the study tool:

```bash
# Structural checks only — no API key needed. Confirms each question's supporting
# source is retrieved and the relevance gate would not wrongly refuse.
python3 scripts/test_answer_quality.py --no-model

# Full run (requires ANTHROPIC_API_KEY): also measures answer accuracy and how
# well the model's stated confidence matches its real accuracy (calibration).
python3 scripts/test_answer_quality.py
```

The structural checks run as part of `scripts/run_pipeline.py`, so retrieval
regressions that would make a known-answerable question unanswerable are caught
automatically. Use this harness to verify that changes (new sources, retriever
tweaks, prompt edits) actually improve answers rather than just feeling better.

## Coverage Report

To see where the corpus and evals are thin relative to the exam blueprint:

```bash
python3 scripts/coverage_report.py
```

It maps `data/metadata/exam_domain_map.yaml` against the corpus and eval suites,
showing each domain's exam weight vs. its corpus share and eval counts (flagging
domains that are `UNDER`-resourced), and lists exam topics that no chunk currently
covers. Uncovered topics are candidates for **new official source documents** —
add them through the ingestion workflow above rather than inventing content.

## RAG Design Principles

This project prioritizes accuracy over broad coverage.

The RAG system should:

- Retrieve before answering.
- Answer only from retrieved context.
- Cite sources when available.
- Refuse when context is insufficient.
- Prefer current official Salesforce content.
- Avoid deprecated terminology unless explicitly labeled.
- Explain certification concepts clearly and directly.
- Separate facts from deductions when needed.

Required refusal phrase:

```text
I don't have enough source-backed information to answer that.
```

## Multiple-Choice Answer Behavior

For multiple-choice certification questions, the system should:

1. Identify the tested Salesforce concept.
2. Retrieve relevant source-backed context.
3. Select the best answer only when supported.
4. Explain why the correct answer is correct.
5. Explain why wrong answers are wrong only when supported.
6. Cite the source.
7. Refuse if the retrieved context is insufficient.

## Current Build Status

This project is in setup phase.

Completed or planned setup items:

- Project folder structure
- Grounding document template
- Source manifest
- Validation script
- Prompt templates
- Eval templates
- Chunking pipeline
- Indexing pipeline
- Retrieval tests
- Answer-quality tests

## Notes for AI Coding Assistants

Before making changes, read:

```text
sf-rag-guidelines.md
```

Any coding assistant should:

- Make the smallest required change.
- Avoid unrelated refactors.
- Preserve folder structure.
- Validate before reporting completion.
- Keep source-grounding and hallucination control as the main priority.
