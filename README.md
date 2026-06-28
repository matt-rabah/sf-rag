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
