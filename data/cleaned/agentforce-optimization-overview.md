---
id: agentforce-optimization-overview
title: About Agent Optimization
source_type: salesforce_help
source_url: https://help.salesforce.com/s/articleView?id=ai.generative_ai_optimize_about.htm&language=en_US&type=5
certification: Agentforce Specialist
exam_domain: Governance & Observability
product_area: Agentforce Platform
topic: Agent Optimization Overview
retrieved_date: 2026-06-28
release_relevance: current
authority: official
status: active
---

# About Agent Optimization

## Summary

Agent Optimization is an Agentforce Observability capability for analyzing real-world sessions, unresolved interactions, knowledge gaps, user intent, response quality, and agent configuration gaps.

## Key Concepts

- Agent Optimization
- Agentforce Observability
- Session Tracing Data Model
- Unresolved interactions
- Knowledge gaps
- Intents
- Intent clusters
- Quality scores
- Session analysis
- Trend identification
- Subagent performance
- Configuration gaps

## Source Content

Agent Optimization analyzes user interactions and agent responses through the Session Tracing Data Model. It helps teams investigate unresolved interactions, identify knowledge gaps, and find opportunities to improve agent effectiveness.

Intents represent sets of interactions within a session that address a specific user request. Agent Optimization generates intents daily, then clusters and tags them weekly across active agents.

Quality scores use an LLM to indicate how relevant an agent’s response was to the user’s request.

Session analysis lets a user inspect what users ask and how agents respond at the intent level.

Trend identification highlights low-performing subagents by quality score, agent misinterpretations, and conversations that were not handled properly. These patterns can point to configuration gaps that need correction.

## Exam Relevance

This source directly supports the Governance & Observability objective about agent optimization. It explains the signals and analysis used to move from observed sessions to targeted agent improvements.

## Notes

Use this source for questions about the purpose of Agent Optimization, the role of intents and quality scores, and how session trends reveal knowledge or configuration gaps.
