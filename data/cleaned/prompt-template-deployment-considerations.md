---
id: prompt-template-deployment-considerations
title: Deployment Considerations for Prompt Templates
source_type: salesforce_help
source_url: https://help.salesforce.com/s/articleView?id=ai.prompt_builder_considerations_deployment.htm&language=en_US&type=5
certification: Agentforce Specialist
exam_domain: Testing, Deployment, & Maintenance
product_area: Prompt Builder
topic: Prompt Template Deployment
retrieved_date: 2026-06-28
release_relevance: current
authority: official
status: active
---

# Deployment Considerations for Prompt Templates

## Summary

Prompt templates can be deployed in managed, unmanaged, or unlocked packages, through change sets, or with the CLI, but template versions and flow input behavior affect deployment success.

## Key Concepts

- Prompt template deployment
- Managed package
- Unmanaged package
- Unlocked package
- Change set
- Salesforce CLI
- Template-triggered flow
- Manual Inputs
- Automatic Inputs
- Template version
- Deployment ordering

## Source Content

Prompt templates can be included in managed, unmanaged, or unlocked packages and deployed through change sets or the Salesforce CLI.

When creating a template-triggered flow, use Manual Inputs. Deploy the prompt template and its flow together in a single deployment.

A flow that uses Automatic Inputs causes deployment failure when a prompt template references it.

If a combined deployment fails, deploy the flow first and then deploy the prompt template separately.

For Salesforce CLI deployment, the prompt template must have at least one template version. A template without a version can’t be deployed through the CLI.

## Exam Relevance

This source directly supports the Testing, Deployment, & Maintenance objective about deploying templates between sandbox and production. It identifies packaging options, flow dependency rules, deployment ordering, and version prerequisites.

## Notes

Use this source for questions about prompt-template deployment methods, template-triggered flow inputs, failure recovery order, and the CLI version requirement.
