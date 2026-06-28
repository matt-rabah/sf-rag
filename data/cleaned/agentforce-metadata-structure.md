---
id: agentforce-metadata-structure
title: "Agent Metadata: A Shallow Dive"
source_type: developer_docs
source_url: https://developer.salesforce.com/docs/ai/agentforce/guide/agent-dx-metadata.html
certification: Agentforce Specialist
exam_domain: Testing, Deployment, & Maintenance
product_area: Agentforce Platform
topic: Agent Metadata Structure
retrieved_date: 2026-06-28
release_relevance: current
authority: official
status: active
---

# Agent Metadata: A Shallow Dive

## Summary

An Agentforce agent is a linked collection of metadata components rather than one standalone file, so reliable deployment requires understanding each component’s role.

## Key Concepts

- AiAuthoringBundle
- Agent Script
- Bot
- BotVersion
- GenAiPlannerBundle
- GenAiPlugin
- GenAiFunction
- GenAiPromptTemplate
- Salesforce DX project
- Package directory

## Source Content

`AiAuthoringBundle` contains the blueprint for an agent. It includes a standard metadata XML file and an `.agent` file written in Agent Script.

`Bot` is the top-level representation of an Agentforce agent. `BotVersion` contains the configuration for a specific version. One agent can have multiple versions, but only one version can be active.

`GenAiPlannerBundle` represents the agent’s reasoning engine and planning configuration. An agent has one `GenAiPlannerBundle`.

`GenAiPlugin` represents a subagent, which groups actions for a particular job. `GenAiFunction` represents an agent action.

Other metadata can be associated with an agent. For example, `GenAiPromptTemplate` represents a prompt template used by agent functionality.

In a Salesforce DX project, agent metadata is stored in a package directory like other Salesforce metadata. Because the components are linked, deployment planning must account for the agent and the assets it references.

## Exam Relevance

This source supports the Testing, Deployment, & Maintenance objective by explaining what must move together when deploying an agent between environments.

## Notes

Use this source for questions about which metadata types represent the agent blueprint, versions, reasoning engine, subagents, actions, and prompt templates.
