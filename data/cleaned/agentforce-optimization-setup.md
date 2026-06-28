---
id: agentforce-optimization-setup
title: Set Up Agent Optimization
source_type: salesforce_help
source_url: https://help.salesforce.com/s/articleView?id=ai.generative_ai_optimize_setup.htm&language=en_US&type=5
certification: Agentforce Specialist
exam_domain: Governance & Observability
product_area: Agentforce Platform
topic: Agent Optimization Setup
retrieved_date: 2026-06-28
release_relevance: current
authority: official
status: active
---

# Set Up Agent Optimization

## Summary

Agent Optimization requires Data 360, an active agent, Einstein Generative AI, Agentforce, a supported Salesforce Standard Data Model version, Session Tracing, and user permissions.

## Key Concepts

- Agent Optimization setup
- Data 360
- Agentforce Session Tracing
- Salesforce Standard Data Model
- Access Agent Optimization permission set
- Data Cloud User permission set
- Active agent
- Voice agents
- Sandbox
- Connector activation
- Data streams

## Source Content

Agent Optimization analyzes sessions and unresolved interactions based on Agentforce Session Tracing data. It supports Agentforce Default, Employee, and Service agents, as well as voice agents. Session analysis and insights appear in English even when sessions use other languages.

Before enabling Agent Optimization, provision and enable Data 360, create an active agent, and turn on Einstein Generative AI and Agentforce.

Verify that the Salesforce Standard Data Model package is version 1.130 or higher. In Einstein Audit, Analytics, and Monitoring Setup, turn on Agentforce Session Tracing. Agent Optimization turns on automatically when Session Tracing is enabled.

Assign users the Access Agent Optimization permission set. Access also requires the Data Cloud User permission set.

For a sandbox, provision Data Cloud, install or upgrade the Salesforce Standard Data Model, reconnect connectors because authentication data is not replicated, activate the AgentOpt connector, and retoggle Agentforce Session Tracing. Data streams then activate automatically.

Storing and querying Agent Optimization data consumes Data 360 credits.

## Exam Relevance

This source supports the Governance & Observability objective about managing and optimizing agents. It defines the technical prerequisites, access controls, and sandbox considerations required before optimization data is available.

## Notes

Use this source for questions about enabling Agent Optimization, its Session Tracing dependency, supported agent types, permission sets, and sandbox connector behavior.
