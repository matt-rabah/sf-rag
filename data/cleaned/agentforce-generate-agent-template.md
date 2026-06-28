---
id: agentforce-generate-agent-template
title: agent generate template
source_type: developer_docs
source_url: https://developer.salesforce.com/docs/platform/salesforce-cli-reference/guide/cli_reference_agent_generate_template.html
certification: Agentforce Specialist
exam_domain: Testing, Deployment, & Maintenance
product_area: Agentforce Platform
topic: Agent Template Packaging
retrieved_date: 2026-06-28
release_relevance: current
authority: official
status: active
---

# agent generate template

## Summary

The Salesforce CLI `agent generate template` command converts an existing agent’s local metadata into template metadata that can be distributed in a second-generation managed package.

## Key Concepts

- Agent template
- Salesforce CLI
- Second-generation managed package
- Bot
- BotVersion
- BotTemplate
- GenAiPlannerBundle
- Scratch org
- Salesforce DX project
- Agent Script limitation

## Source Content

The template workflow starts with an agent created and tested in a namespaced scratch org. Retrieve the agent metadata into a Salesforce DX project before generating the template.

Agents used by the command are defined by `Bot`, `BotVersion`, and `GenAiPlannerBundle` metadata. The command uses these local files to create a `BotTemplate` file for a selected agent and version.

The command also generates a `GenAiPlannerBundle` that references the `BotTemplate`. Package these files in a second-generation managed package to share the template between orgs or through AppExchange.

Specify the path to the agent’s `Bot` metadata file, the required agent version, the output directory, and the namespaced source scratch org. The matching `BotVersion` file must exist in the local project.

The command currently does not work for agents created from an Agent Script file. Those agents can’t currently be packaged as agent templates with this workflow.

## Exam Relevance

This source directly supports the Testing, Deployment, & Maintenance objective about deploying an agent template. It explains the source-org, metadata, generation, and managed-package sequence, plus a release-sensitive limitation.

## Notes

Use this source for questions about generating `BotTemplate` metadata, second-generation packaging, required input files, and the current Agent Script restriction.
