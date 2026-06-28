---
id: data-360-hybrid-search-features
title: Hybrid Search Features in Data 360
source_type: salesforce_help
source_url: data_360_6-28-2026.pdf
certification: Agentforce Specialist
exam_domain: Data 360 Fundamentals
product_area: Data 360
topic: Hybrid Search
retrieved_date: 2026-06-28
release_relevance: current
authority: official
status: active
---

# Hybrid Search Features in Data 360

## Summary

Data 360 provides advanced features for hybrid search, including Hybrid Search Autodrop and Hybrid Search Fusion Ranker, to improve search accuracy and precision. Search Index Configuration is used to generate the necessary chunks and vector embeddings.

## Key Concepts

- Hybrid Search
- Hybrid Search Autodrop
- Hybrid Search Fusion Ranker
- Search Index Configuration
- Vector Search
- Keyword Search
- RAG

## Source Content

**Hybrid Search**
The process in which the results from a keyword search and vector search are merged and ranked to generate the most relevant response. Hybrid search generates two result sets, one based on keyword matching and the other based on semantic similarity. A hybrid search fusion ranker model then reranks these results into a single ranking to be used in Retrieval Augmented Generation (RAG).

**Hybrid Search Autodrop**
Hybrid search autodrop dynamically filters out results that show a sharp decrease in relevance scores for a search query. This increases the precision of search results for your prompts and RAG use cases.

**Hybrid Search Fusion Ranker**
A fusion ranking model that reranks the merged results retrieved from Data 360 hybrid search to surface the most relevant results for a search query.

**Search Index Configuration**
A process in Data 360 that generates chunks and vector embeddings from unstructured data.

## Exam Relevance

This source supports the Data 360 Fundamentals domain of the Agentforce Specialist exam by defining advanced features for optimizing hybrid search, such as autodrop and fusion ranking.
