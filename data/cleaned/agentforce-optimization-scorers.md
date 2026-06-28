---
id: agentforce-optimization-scorers
title: Scorers and Custom Scorers (Beta)
source_type: salesforce_help
source_url: https://help.salesforce.com/s/articleView?id=ai.generative_ai_optimize_scorers.htm&language=en_US&type=5
certification: Agentforce Specialist
exam_domain: Governance & Observability
product_area: Agentforce Platform
topic: Agent Optimization Scorers
retrieved_date: 2026-06-28
release_relevance: current
authority: official
status: active
---

# Scorers and Custom Scorers (Beta)

## Summary

Scorers evaluate Agentforce sessions and produce scores, text dimensions, and numeric measures that appear in Agent Optimization and Analytics.

## Key Concepts

- Scorers
- Custom scorers
- Standard scorers
- Agentforce Optimization
- Agent Analytics
- Next Gen Testing
- Scorer Hub
- Session-level scoring
- Sampling rate
- LLM-as-a-judge
- Expression-based logic
- Post-session evaluation

## Source Content

Scorers are evaluation components in Agentforce Studio. They analyze sessions and generate scores, text dimensions, and numeric measures for Agent Optimization and Analytics.

Salesforce supplies standard scorers. Standard scorers include Abandonment Score, Deflection Score, and Quality Score. A standard scorer can’t be edited directly; clone it to create a customized version.

Organizations can define custom scorers for business-specific criteria. Custom scorers use either an LLM-as-a-judge prompt or expression-based logic. Create and refine them in Next Gen Testing, then manage and activate them in the Scorer Hub.

A scorer runs against a configurable percentage of sessions. Scoring occurs after the session ends, so it does not add latency to the live conversation. The resulting labels and scores appear in Agent Optimization and Analytics.

During beta, custom scorers support session-level evaluation and do not support Agentforce Employee Agent. Testing Center sessions are not scored because they do not receive the end timestamp that triggers custom scorer evaluation.

## Exam Relevance

This source supports the Governance & Observability objective about agent analytics and optimization. It explains how standard and business-specific evaluations turn production sessions into measurable improvement signals.

## Notes

Use this source for questions about standard versus custom scorers, scorer execution timing, sampling, output types, beta limitations, and where scorer results appear.
