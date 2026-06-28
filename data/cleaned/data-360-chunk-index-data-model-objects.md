---
id: data-360-chunk-index-data-model-objects
title: Chunk and Index Data Model Objects
source_type: salesforce_help
source_url: https://help.salesforce.com/s/articleView?id=data.c360_a_search_index_chunk_index_dmo.htm&language=en_US&type=5
certification: Agentforce Specialist
exam_domain: Data 360 Fundamentals
product_area: Data 360
topic: Chunk and Index Data Model Objects
retrieved_date: 2026-06-28
release_relevance: current
authority: official
status: active
---

# Chunk and Index Data Model Objects

## Summary

When a search index configuration is created in Data 360, Data 360 creates additional objects to store chunked content and generated embeddings.

## Key Concepts

- Search index configuration
- Chunk data model object
- Chunk DMO
- CDMO
- Index data model object
- Index DMO
- IDMO
- Chunked content
- Vector embeddings
- Data 360
- Search index

## Source Content

When you create a search index configuration, Data 360 creates two additional data model objects: a chunk data model object and an index data model object.

These objects store the corresponding data and generated embeddings in Data 360.

The chunk data model object, or CDMO, stores chunked content for each field from a chunked object.

The index data model object, or IDMO, stores generated vector embeddings.

When a search index configuration creates data lake objects, chunk data lake objects are given the Content data category, and index data lake objects are given the Vector Embedding data category.

## Exam Relevance

This source supports the Data 360 Fundamentals domain of the Salesforce Certified Agentforce Specialist exam.

It is relevant because the exam guide includes chunking, indexing, and retrievers. This source explains the objects Data 360 uses to store chunked content and generated embeddings during indexing.

## Notes

Use this source for questions about what Data 360 creates during search index configuration, where chunked content is stored, where vector embeddings are stored, and the difference between CDMO and IDMO.
