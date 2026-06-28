---
id: data-360-retriever-types
title: Retriever Types in Data 360
source_type: salesforce_help
source_url: data_360_6-28-2026.pdf
certification: Agentforce Specialist
exam_domain: Data 360 Fundamentals
product_area: Data 360
topic: Retrievers
retrieved_date: 2026-06-28
release_relevance: current
authority: official
status: active
---

# Retriever Types in Data 360

## Summary

Retrievers act as a logical layer between the search service and knowledge retrieval-powered solutions. Different types of retrievers, such as dynamic retrievers and ensemble retrievers, support various use cases.

## Key Concepts

- Retriever
- Dynamic Retriever
- Ensemble Retriever
- Search Service
- Knowledge Retrieval
- RAG

## Source Content

**Retriever**
A logical layer between the search service and knowledge retrieval-powered solutions, such as RAG (Retrieval Augmented Generation) implementations. It defines the runtime search and retrieval configuration for an application, agent, prompt templates, and other solution components. A retriever serves as a reusable, versioned, and packageable artifact that simplifies the setup of knowledge retrieval with search-based grounding for agents, Agentforce data libraries, prompt templates, with Apex, or in Flow.

**Dynamic Retriever**
A dynamic retriever defines a placeholder variable for a value that’s specified in a prompt template at run time.

**Ensemble Retriever**
A collection of individual retrievers. When you run an ensemble retriever, it executes the individual retrievers, combines their results into a single list, reranks the list according to relevance to the search request, and returns the most relevant information to the prompt template or agent.

## Exam Relevance

This source supports the Data 360 Fundamentals domain of the Agentforce Specialist exam by defining what retrievers are and detailing specific types like Dynamic Retrievers and Ensemble Retrievers.
