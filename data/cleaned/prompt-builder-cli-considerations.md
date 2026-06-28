---
id: prompt-builder-cli-considerations
title: Salesforce CLI Considerations for Prompt Templates
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

# Salesforce CLI Considerations for Prompt Templates

## Summary

Understand the limits and behaviors that are related to metadata component dependencies and deployment when using Salesforce CLI with Prompt Templates.

## Key Concepts

- Prompt Builder
- Prompt templates
- Salesforce CLI
- Deployment
- GenAiPromptTemplate metadata
- `sf project deploy start`
- `sf project retrieve start`

## Source Content

Understand the limits and behaviors that are related to metadata component dependencies and deployment when using Salesforce CLI with Prompt Templates.

**Use Salesforce CLI with Prompt Templates**

Prompt templates are represented in an org with the `GenAiPromptTemplate` metadata type. Use standard Salesforce CLI commands to deploy and retrieve specific GenAiPromptTemplate components between your DX project and org.

Deploy:
`sf project deploy start --metadata GenAiPromptTemplate:TemplateName --target-org myorg@username.com`

Retrieve:
`sf project retrieve start --metadata GenAiPromptTemplate:TemplateName --target-org myorg@username.com`

Replace `TemplateName` with the name of your prompt template, and `myorg@username.com` with the unique username or alias of your org.

**Activate and Deactivate Prompt Templates**

- You can use `<versionIdentifier>` in `<activeVersionIdentifier>` to activate a template, or you can activate a template in the UI and retrieve it for correct XML.
- If a template is in use, block deactivation of a version unless another version is activated.
- If a prompt template version is published and not in use, any version can be activated or deactivated.
- If a template isn't in use, version deactivation is allowed without needing to activate another version.

**Create New Prompt Templates**

- After adding a new template, get the template because `<versionIdentifier>` is generated automatically after the version is created.
- When you have a template with `<versionIdentifier>` and `<activeVersionIdentifier>`, you can deploy that to another org. The versionIdentifer ensures that there's no need for you to deploy or retrieve it for all orgs in CI/CD pipelines.

**Delete Prompt Templates**

- Prompt templates can't be deleted via CLI.
- Prompt template versions can be deleted with the CLI. When deleted, it's removed from the version in XML.
- A template version can be deleted from the XML and deployed via CLI. The deleted version is deleted in the target org unless that version is active and in use.
- If a template is used with an active version, it can’t be deleted.

**Deploy Prompt Templates**

- You must have at least 1 template version to deploy the template.

**Modify Prompt Templates**

- If a prompt template version is published and not in use, it can’t be modified.
- Any published version can't be modified. The deploy will succeed, and published versions are skipped.
- If you manually set `<versionIdentifier>` and have duplicated it, the new and old versions will overwrite each other, if those versions are in draft status. Otherwise, the first published version stays and the second one is skipped, as published versions are immutable.

**Other Considerations**

- If a template has been overridden, users aren't allowed to override it again with a changeset, CLI, or Connect API.

## Exam Relevance

This source supports the Prompt Builder domain of the Salesforce exams.

It is relevant because the exam requires understanding how to deploy prompt templates with the Salesforce CLI, which metadata type represents them (`GenAiPromptTemplate`), and managing the XML `<versionIdentifier>`.

## Notes

Use this source for questions about deploying prompt templates via CLI, modifying XML elements for prompt templates, and the behavior of draft and published versions when deploying via CLI.
