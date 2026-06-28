# SF-RAG Project Guidelines

These rules apply to all work in this project.

## 1. Project Goal

The goal is to build a low-hallucination Salesforce certification-prep RAG system.

The system should help answer Salesforce certification questions using source-backed grounding from
official and trusted materials.

This is not a broad Salesforce chatbot. It is a certification-focused study and explanation tool.

## 2. Grounding Quality Comes First

The source corpus is more important than the model.

Every grounding document must:

- Use Markdown with YAML frontmatter.
- Preserve the original meaning of the source.
- Include source metadata.
- Include the original source URL when available.
- Identify the relevant certification, exam domain, product area, and topic.
- Clearly mark deprecated, archived, uncertain, or needs-review content.
- Pass validation before it is chunked or indexed.

Do not index documents that fail validation.

## 3. Required Grounding Document Format

Every file in `data/cleaned/` must include YAML frontmatter with these fields:

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

The document body must contain useful cleaned content. Empty or placeholder-only documents must not
be indexed.

## 4. Preferred Source Authority

Prefer sources in this order:

1. Official Salesforce exam guides
2. Salesforce Help
3. Salesforce Developer documentation
4. Salesforce Trailhead
5. Salesforce release notes
6. Personal notes based on verified sources
7. Practice questions and corrections

Third-party sources should be marked clearly and should not override official Salesforce sources.

## 5. Current Salesforce Terminology

Use current Salesforce terminology when describing concepts.

Preferred terms:

- Agentforce Data Library
- Data 360, when referring to current product positioning
- Data Cloud, only when the official source, API name, object name, or feature label specifically
  uses Data Cloud
- AI, not Al
- 100 MB, not l00 MB

Do not include deprecated product names, model names, roadmap claims, or outdated processes unless
they are explicitly labeled as deprecated, archived, or historical.

## 6. Simplicity First

Build the smallest reliable version before adding complexity.

Do not add:

- unnecessary frameworks
- premature local model support
- multi-certification support before one certification works
- speculative metadata fields
- unnecessary abstractions
- broad agent workflows before retrieval is validated

Prefer:

- Markdown with YAML frontmatter
- JSONL chunks
- simple Python scripts
- explicit validation
- hybrid retrieval
- source-backed answer prompts
- repeatable evals

## 7. Surgical Changes

When editing this project:

- Touch only the files required for the task.
- Do not reformat unrelated files.
- Do not rename folders unless explicitly asked.
- Do not change the metadata schema casually.
- Do not refactor scripts unless the task requires it.
- Preserve existing file paths and naming conventions.

Every changed line should connect directly to the requested task.

## 8. Validation Before Indexing

The ingestion flow should be:

1. Add source to `data/metadata/source_manifest.yaml`.
2. Create or clean Markdown in `data/cleaned/`.
3. Validate the Markdown frontmatter and body.
4. Chunk only valid documents.
5. Export chunks as JSONL.
6. Index only validated chunks.
7. Test retrieval before testing answer generation.

A document that fails validation must not be chunked or indexed.

## 9. Chunking Rules

Chunk by concept, not by arbitrary size alone.

Each chunk should preserve enough context to answer a certification-style question.

Good chunks usually include:

- the concept name
- the definition
- key rules or limitations
- relevant setup/process steps
- exam relevance
- source metadata

Avoid chunks that are too small to stand alone or too large to retrieve precisely.

## 10. Hallucination Control

The agent must not answer certification questions from general knowledge when source-backed context
is missing.

For RAG answers:

- Retrieve first.
- Answer only from retrieved context.
- Cite the source.
- Refuse when the retrieved context is insufficient.
- Separate facts from deductions when relevant.
- Explain wrong multiple-choice answers only when the source supports the explanation.

Required refusal:

> I don't have enough source-backed information to answer that.

## 11. Multiple-Choice Question Rules

For certification-style multiple-choice questions, the agent should:

1. Identify the tested Salesforce concept.
2. Retrieve the relevant source-backed context.
3. Select an answer only when supported by the retrieved context.
4. Explain why the correct answer is correct.
5. Explain why the incorrect answers are wrong only when supported by the retrieved context.
6. Cite the source.
7. Refuse if the retrieved context is insufficient.

The agent should not guess based on general Salesforce knowledge.

## 12. Evaluation Rules

Every meaningful change should be evaluated against test questions.

Use eval files in `evals/` to test:

- whether the retriever finds the expected source
- whether the answer is source-backed
- whether the agent refuses when context is insufficient
- whether multiple-choice distractors are handled correctly
- whether outdated or deprecated content is avoided

Retrieval quality should be tested before answer quality.

## 13. Success Criteria

A task is complete only when there is a clear success condition.

Examples:

- “Add a grounding template” means the template exists and matches the required metadata fields.
- “Validate grounding docs” means invalid files fail with clear errors.
- “Chunk documents” means every output JSONL record includes chunk text, source ID, metadata, and
  source URL.
- “Improve retrieval” means test questions retrieve the expected source chunks.
- “Improve answer quality” means answers are grounded, cited, and refuse when evidence is weak.

## 14. Working Style for AI Coding Assistants

When using an AI coding assistant, require it to:

1. Restate the task.
2. Identify the files it will change.
3. Make the smallest required change.
4. Avoid unrelated refactors.
5. Run or describe the validation check.
6. Report what passed, failed, or remains uncertain.

Do not allow broad, unsupervised rewrites.
