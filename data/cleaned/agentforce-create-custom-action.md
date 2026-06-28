---
id: agentforce-create-custom-action
title: Create a Custom Action
source_type: salesforce_help
source_url: https://help.salesforce.com/s/articleView?id=ai.agent_actions_custom.htm&language=en_US&type=5
certification: Agentforce Specialist
exam_domain: AI Agents
product_area: Agentforce Platform
topic: Custom Agent Actions
retrieved_date: 2026-06-28
release_relevance: current
authority: official
status: active
---

# Create a Custom Action

## Summary

Custom agent actions let you connect an agent to business-specific Salesforce functionality.

A custom action can call invocable methods, REST Apex classes, external services, autolaunched flows, MuleSoft APIs, or prompt templates.

## Key Concepts

- Custom agent action
- Agentforce Builder
- Asset library
- Invocable methods
- REST Apex classes
- External services
- Autolaunched flows
- MuleSoft APIs
- Prompt templates
- Reference action
- Permissions
- Reasoning actions
- Draft agent version

## Source Content

A custom action can call invocable methods and REST Apex classes, external services, autolaunched flows, MuleSoft APIs, or prompt templates.

Before creating a custom action, create the underlying Salesforce functionality that the agent action will use.

When you create a custom action from an agent in Agentforce Builder, the action is available only to that agent. Changes apply only to that agent version.

To make a custom action available to multiple agents, versions, and subagents, create it in the asset library.

Access to a custom agent action depends on the type of Salesforce functionality that it references.

For example, if a custom action is built using a flow, the custom action follows the permissions, field-level security, and sharing settings configured in the flow.

When creating a custom action from the asset library, choose the reference action type, such as a flow or prompt template, and then select the reference action.

A custom action is automatically added to a subagent's reasoning actions, making it available for the agent to select during reasoning with an LLM.

## Exam Relevance

This source supports the AI Agents domain of the Salesforce Certified Agentforce Specialist exam.

It is relevant because the exam requires understanding how custom actions extend agent capability, what underlying functionality a custom action can reference, and how permissions and asset availability affect action behavior.

## Notes

Use this source for questions about what custom actions can call, when to create actions in Agentforce Builder versus the asset library, how reference actions work, and why permissions matter for custom actions.
