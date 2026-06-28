---
id: agentforce-optimization-intents
title: Use Intents in Agent Optimization
source_type: salesforce_help
source_url: https://help.salesforce.com/s/articleView?id=ai.generative_ai_optimize_intent_use.htm&language=en_US&type=5
certification: Agentforce Specialist
exam_domain: Governance & Observability
product_area: Agentforce Platform
topic: Agent Optimization Intents
retrieved_date: 2026-06-28
release_relevance: current
authority: official
status: active
---

# Use Intents in Agent Optimization

## Summary

Agent Optimization generates intents from closed sessions and clusters semantically similar intents so teams can analyze recurring user objectives and agent-response patterns.

## Key Concepts

- Agent Optimization intents
- Closed sessions
- Intent pipeline
- Clustering pipeline
- Shared user objectives
- Cluster tags
- Semantic similarity
- Minimum cluster size
- Untagged intents
- Session trace
- Pipeline timing

## Source Content

An intent represents a set of interactions within a session that addresses a specific user request. The intent pipeline analyzes closed sessions and generates intents. The clustering pipeline groups intents that express similar user goals.

A cluster and its tag require at least 10 semantically similar intents. Intents outside a qualifying cluster do not receive a tag and do not appear in the session trace as tagged intent instances.

The system can reconsider untagged intents in later clustering runs. Clustering generally evaluates about the last month of intents and runs about once per week.

A session closes explicitly or is assumed closed after three hours of inactivity. The intent scheduler runs every three hours. The intent pipeline usually takes four to five hours and can take up to 24 hours.

After the first successful intent pipeline run, the system waits before starting clustering so enough intent data can accumulate. Low conversation volume can delay useful clusters.

## Exam Relevance

This source supports the Governance & Observability objective about agent optimization. It explains how session activity becomes intent-level insight and why missing or delayed cluster tags do not necessarily indicate missing session data.

## Notes

Use this source for questions about intent generation, clustering thresholds, untagged intents, session-close timing, and when optimization insights become available.
