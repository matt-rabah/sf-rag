---
id: agentforce-deploy-metadata-new-org
title: Use Metadata to Move an Agent to a New Org
source_type: developer_docs
source_url: https://developer.salesforce.com/docs/ai/agentforce/guide/agent-dx-deploy-metadata.html
certification: Agentforce Specialist
exam_domain: Testing, Deployment, & Maintenance
product_area: Agentforce Platform
topic: Agent Metadata Deployment
retrieved_date: 2026-06-28
release_relevance: current
authority: official
status: active
---

# Use Metadata to Move an Agent to a New Org

## Summary

Move an Agentforce agent from a sandbox to production by retrieving its metadata into a Salesforce DX project and deploying that metadata, its dependencies, and a valid agent-user configuration to the target org.

## Key Concepts

- Salesforce CLI
- Source org
- Target org
- Sandbox
- Production
- package.xml
- AiAuthoringBundle
- Bot
- BotVersion
- GenAiPlannerBundle
- Agent user
- Dependent metadata

## Source Content

Authorize the source and target orgs with Salesforce CLI. Einstein and Agentforce must be enabled in both orgs, and the deployment user needs the permissions required to publish and preview agents.

Create a Salesforce DX project and a `package.xml` manifest that defines the agent metadata and required dependencies. Include metadata used by the agent, such as flows, prompt templates, Apex classes, and Data 360 dependencies.

A draft, uncommitted agent is represented by `AiAuthoringBundle` and remains editable. A committed agent is represented by `AiAuthoringBundle`, `Bot`, and `BotVersion` and isn’t editable. A legacy agent uses `Bot` and `BotVersion`.

Retrieve the selected metadata from the source org and deploy it to the target org. Avoid broad wildcards for flows, prompt templates, and Apex classes because they can retrieve excessive metadata and cause long deployments or timeouts.

Before using the deployed agent, assign its agent user in the target org. Source and target usernames differ. The target agent user must have the permissions required by the agent’s actions and data access.

Do not modify retrieved agent metadata directly because deploying edited metadata can corrupt the target org.

## Exam Relevance

This source directly supports the Testing, Deployment, & Maintenance objective about moving an agent from sandbox to production. It covers org prerequisites, metadata composition, dependency selection, version state, and target-org user configuration.

## Notes

Use this source for questions about the end-to-end agent metadata deployment process, draft versus committed metadata, dependency inclusion, and post-deployment agent-user setup.
