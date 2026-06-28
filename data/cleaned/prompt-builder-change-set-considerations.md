---
id: prompt-builder-change-set-considerations
title: Change Set Considerations for Prompt Templates
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

# Change Set Considerations for Prompt Templates

## Summary

Before you use change sets to deploy a prompt template, understand the limits and behaviors that are related to component dependencies and deployment.

## Key Concepts

- Prompt Builder
- Prompt templates
- Change sets
- Deployment
- Draft status
- Published status

## Source Content

Before you use change sets to deploy a prompt template, understand the limits and behaviors that are related to component dependencies and deployment.

**Activate and Deactivate**

- Activating a prompt template changes the version status from Draft to Published. When a version is published, it can't be changed to a draft.
- Prompt template versions can be activated or deactivated.
- A version doesn’t auto-activate during deployment between multiple orgs unless the Deploy Prompt Templates permission is enabled in the target org. This permission is only applicable to changesets and can be found in Setup under Einstein Setup.
- If the prompt template is in use, a version can’t be deactivated unless another version is active.
- If a prompt template is in use, the active version can't be deleted.
- If a flow is referenced in a prompt template and deployed, the flow isn't auto-activated. Follow the flow guidelines for auto-activation. If a prompt template is executed with an inactive flow, you receive an error at runtime.

**Other Considerations**

- Any published prompt template version can’t be modified and is skipped when it’s deployed.
- If a template is overridden, users aren't allowed to override it again with a changeset, command-line interface (CLI), or Connect API.
- Prompt templates can’t be deleted via changeset.
- When you deploy a template with custom large language model (LLM) configuration, verify that the target org has a model with the same name. If the model name doesn't match, the deployment fails.
- When a template is deployed by using a changeset, all versions—active or inactive—are included in the deployment.
- Add all resources in the changeset, and then add dependencies.

## Exam Relevance

This source supports the Prompt Builder domain of the Salesforce exams.

It is relevant because the exam requires understanding how prompt templates are deployed, what statuses they can be in, and how to manage their lifecycle across orgs using change sets.

## Notes

Use this source for questions about migrating or deploying prompt templates using change sets, activation behaviors upon deployment, and overriding restrictions.
