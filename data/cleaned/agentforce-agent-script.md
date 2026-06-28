---
id: agentforce-agent-script
title: Agent Script
source_type: developer_docs
source_url: https://developer.salesforce.com/docs/ai/agentforce/guide/agent-script.html
certification: Agentforce Specialist
exam_domain: AI Agents
product_area: Agentforce Platform
topic: Agent Script
retrieved_date: 2026-06-28
release_relevance: current
authority: official
status: active
---

# Agent Script

## Summary

Agent Script is the language for building agents in the new Agentforce Builder.

Agent Script combines the flexibility of natural language instructions for conversational tasks with the reliability of programmatic expressions for business rules, so agents do not rely solely on interpretation by an LLM.

## Key Concepts

- Agent Script
- Agentforce Builder
- Hybrid reasoning
- Deterministic behavior
- Programmatic expressions
- Conditional expressions
- If/else conditions
- Transitions
- Action chaining
- Variables
- Subagents
- Canvas view
- Script view
- Template expressions

## Source Content

Agent Script is the language for building agents in Agentforce Builder. Script combines the flexibility of natural language instructions for handling conversational tasks with the reliability of programmatic expressions for handling business rules.

In script, you use expressions to define if/else conditions, transitions, and other logic; set, modify, and compare variables; and select subagents and actions.

You can build predictable, context-aware agent workflows that don't rely solely on interpretation by an LLM. For example, you can use script to control when your agent transitions from one subagent to another or when actions are run in a particular sequence, sometimes called action chaining.

Agentforce Builder gives you several ways to write Agent Script. You can chat with Agentforce and explain what you want your agent to do, and Agentforce converts your request into subagents, actions, instructions, and other expressions. In Canvas view, Agent Script is summarized into easily understandable blocks that you can expand to view the underlying script, and you can edit your agent using quick action shortcuts. Advanced users can switch to Script view to write and edit script directly, with developer-friendly aids like syntax highlighting, autocompletion, and validation.

Agent Script preserves the conversational skills and complex reasoning ability derived from natural language prompts, and it adds the determinism of programmatic instructions. In Agent Script, you can define specific areas where an LLM is free to make reasoning decisions, specific areas where the agent must execute deterministically, variables to reliably store information about the agent's current state rather than relying on LLM context memory, conditional expressions that determine the agent's execution path, and the conditions under which the agent transitions to a new subagent.

## Exam Relevance

This source supports the AI Agents domain of the Salesforce Certified Agentforce Specialist exam.

It is relevant because the exam covers Agent Script, hybrid reasoning, deterministic behavior, template expressions, and how agents combine LLM reasoning with programmatic control.

## Notes

Use this source for questions about Agent Script, the scripting language in Agentforce Builder, deterministic versus LLM-driven behavior, conditional expressions, subagent transitions, action chaining, and how Canvas and Script views relate to Agent Script.
