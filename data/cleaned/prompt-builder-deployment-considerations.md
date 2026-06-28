---
id: prompt-builder-deployment-considerations
title: Deployment Considerations for Prompt Templates
source_type: salesforce_help
source_url: quickstart_your_einstein_generative_ai_solution_6-28-2026.pdf
certification: Agentforce Specialist
exam_domain: Testing, Deployment, & Maintenance
product_area: Prompt Builder
topic: Deploying Prompt Templates
retrieved_date: 2026-06-28
release_relevance: current
authority: official
status: active
---

# Deployment Considerations for Prompt Templates

## Summary

Include a prompt template in managed, unmanaged, or unlocked packages. Before you deploy a package that contains a prompt template, in changesets or on the CLI, understand the limitations and behaviors.

## Key Concepts

- Prompt Builder
- Prompt templates
- Deployment
- Packages
- Template-triggered flows
- CLI deployment

## Source Content

Include a prompt template in managed, unmanaged, or unlocked packages. Before you deploy a package that contains a prompt template, in changesets or on the CLI understand the limitations and behaviors.

**Deploy Packages**

- Use Manual Inputs when creating Template-triggered Flows. Deploy the prompt and the flow together in a single deployment.
- Flows with Automatic Inputs will cause a deployment to fail if a template references them.
- If a deployment fails, deploy the flow first, and then deploy the template separately.
- To deploy a package using the CLI, you must have at least one template version to deploy the template.

## Exam Relevance

This source supports the Prompt Builder domain of the Salesforce exams.

It is relevant because the exam tests the ability to troubleshoot deployment failures, such as failures caused by Template-triggered Flows with Automatic Inputs, and the correct order of operations for deploying templates and flows.

## Notes

Use this source for questions about troubleshooting prompt template deployments, the requirement to use Manual Inputs for Template-triggered Flows, and general package deployment rules for prompt templates.
