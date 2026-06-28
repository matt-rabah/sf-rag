---
id: agentforce-enterprise-agentic-architecture
title: Enterprise Agentic Architecture and Design Patterns
source_type: developer_docs
source_url: https://architect.salesforce.com/docs/architect/fundamentals/guide/enterprise-agentic-architecture.html
certification: Agentforce Specialist
exam_domain: Multi-Agent Orchestration
product_area: Agentforce Platform
topic: Enterprise Agentic Architecture
retrieved_date: 2026-06-28
release_relevance: current
authority: official
status: active
---

# Enterprise Agentic Architecture and Design Patterns

## Summary

Enterprise agentic architecture describes how multiple agents can collaborate across an enterprise architecture.

One important pattern is SOMA, or Single Org, Multiple Agents, where multiple agents collaborate within one Salesforce org using shared governance and data.

## Key Concepts

- Agentforce
- Multi-Agent Orchestration
- Enterprise agentic architecture
- SOMA
- Single Org, Multiple Agents
- Supervisor agent
- Specialist agents
- Shared governance
- Shared data
- Agent handoff
- Agent collaboration
- MCP
- MCP wrapper
- MuleSoft
- External functionality

## Source Content

SOMA means Single Org, Multiple Agents.

In a SOMA pattern, multiple agents collaborate within one Salesforce org that uses shared governance and data.

In Agentforce, a Supervisor agent can act as a single front door.

The Supervisor agent routes requests to Specialist agents within the org.

For external functionality, agents can use the Agentforce MCP Client with MuleSoft acting as an MCP-wrapper for APIs that are not MCP-enabled.

This architecture supports multi-agent collaboration while keeping governance, data, and orchestration patterns controlled.

## Exam Relevance

This source supports the Multi-Agent Orchestration domain of the Salesforce Certified Agentforce Specialist exam.

It is relevant because the exam guide includes SOMA, MCP, A2A, and multi-agent orchestration concepts. This source directly supports SOMA and MCP-wrapper architecture.

## Notes

Use this source for questions about SOMA, Supervisor agents, Specialist agents, shared governance and data, agent handoffs, and MCP-wrapper patterns for external functionality.
