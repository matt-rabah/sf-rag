---
id: prompt-builder-packaging-considerations
title: Packaging Considerations for Prompt Templates
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

# Packaging Considerations for Prompt Templates

## Summary

Include a prompt template in managed, unmanaged, or unlocked packages. Before you create, update, or deploy a package that contains a prompt template, understand the limitations and behaviors of packages.

## Key Concepts

- Prompt Builder
- Prompt templates
- Managed, unmanaged, unlocked packages
- Custom objects
- Overridable templates
- Second-generation (2GP) packages

## Source Content

Include a prompt template in managed, unmanaged, or unlocked packages. Before you create, update, or deploy a package that contains a prompt template, understand the limitations and behaviors of packages.

**Create Packages**

- Prompt templates that include a flow with a custom object input may cause package installation to fail, as packaging for prompt flows with custom objects isn't supported.
- Include only published versions. Draft versions can be added to the package, but they aren’t installed in customer orgs for managed packages.
- Any future changes to a published version are skipped during upgrade without error.
- If a published version is active and it’s different from the current version, it’s auto-activated in the customer’s organization.
- If no versions are published, don’t package the template. If you package a template without a published version, any installation or upgrade fails because of an empty template.
- Prompt templates with custom models can’t be packaged.
- If you include an Apex class in a prompt template and package it, the class must be global.
- For unmanaged, unlocked, or managed packages, avoid packaging templates that override any out-of-the-box (OOTB) template. Packaged templates can optionally be configured as overridable, which allows subscribers to create local versions of the template.
- Retrievers like Data Search and Data Graphs aren’t included in packages. Instead, they’re part of a data kit in Data Cloud. Salesforce Independent Software Vendors (ISVs) are encouraged to provide retrievers to the customer, or the installation fails because of missing metadata.
- New versions can be added to an existing template, but previously published versions can’t be modified or deleted. For overridable templates, subscribers can create additional override versions that customize the packaged template.
- New versions can be activated, and old versions can be deactivated. If a subscriber activates an override version, that version takes precedence over the publisher’s active version.
- Customers can’t edit packaged templates directly. However, if the publisher enables overridable templates, customers can create a new version that overrides the packaged template. Customers can also clone the template to create an independent custom template.
- A template with no active version can be delivered, but customers can't use it until a version is activated. Customers can clone the template to create an independent custom template, or if the template is configured as overridable they can create a local override version.
- `ManagePromptTemplates` permission must be assigned while creating second-generation (2GP) package versions.

**Install and Upgrade Installed Prompt Templates**

- In Einstein Setup, if Add or Require Inputs After Activation isn’t enabled and you change inputs between template versions, the package installation fails with the error: 'This app can't be upgraded.'
- Before installing or upgrading a package in production, test installation or upgrade in sandbox and test.
- Customers can't deactivate a version after installation or upgrade.
- You can’t overwrite a published prompt template version.
- If the prompt template model is hidden, the existing template works as intended. However, if the template is cloned, the model won’t be available for use.
- For active versions, auto-activate them in the customer organization. Always test changes in sandboxes before installing or upgrading a package.
- Einstein Generative AI must be activated for installation of packages with Prompt templates otherwise installation fails.
- Flows aren't auto-activated when a package is installed. Flows follow the standard activation process for managed packages that's established.
- Partners can deactivate a template. However, if that template is in use for the customer, the upgrade fails. To upgrade the package, customers must remove that template from use.
- If you package a template with a custom LLM model configuration, verify your customer org has a model with the same name, otherwise installation or upgrade fails.
- Custom fields on Dynamic Forms-enabled Lightning pages can reference prompt templates. If you install a managed package containing a prompt template that is referenced by a custom field on a Dynamic Forms-enabled Lightning page, and that prompt template references a custom field with a namespace that is different from the Lightning page's namespace, package installation can fail.

**Delete Installed Prompt Templates**

- Versions can't be deleted from a managed template.
- A managed template can be deleted from a 2GP package, but it isn't deleted on the customer's org. Customers see the deprecated templates and have the option to delete them.

**Overridable Prompt Templates**

Publishers can configure packaged prompt templates to be overridable. When a template is overridable, subscribers can create local versions of the template and customize the prompt text or configuration. Although these custom versions are linked to the template, they remain separate. Any update to the published version doesn’t impact the custom versions.

Subscriber override versions appear in the version picker alongside publisher-managed versions. If a subscriber activates an override version, that version becomes the active version in the subscriber organization. However, activating the override does not deactivate the packaged version, the package version is automatically activated. This behavior preserves flows, especially packaged ones, which can depend on this template being active.

Publisher versions remain managed by the package and continue to receive updates through package upgrades.

**Considerations For Partners**

- To allow a template to be overridable, use `<overridable>true</overridable>`.
- Once a template’s overridable setting is true and installed in the customer org, the setting cannot be undone. The upgrade fails with an error.
- Deleting a packaged template from a package marks it as deletable in the customer org. If a customer deletes that template, and the template isn’t being used, their customer overrides are also deleted.
- Subscribers can use the Save as a new version option to override the template.
- If custom version is active and the template is being used, then it cannot be deleted.
- If custom version is active, the template is being used, but there is an active managed package version then deactivating custom version will fall back to that version.
- If custom version is active, the template is being used, but there is no active managed package version then deactivation will fail.
- The Template Overrides option in Prompt Builder appears only in orgs with a namespace.
- When you clone an overridable template, the cloned template isn't overridable. Explicitly set the new template as overridable.

## Exam Relevance

This source supports the Prompt Builder domain of the Salesforce exams.

It is relevant because the exam requires understanding the intricacies of packaging prompt templates, managing 2GP packages, handling overridable templates, and ensuring dependencies like custom objects or Data Cloud retrievers are properly handled.

## Notes

Use this source for questions about packaging limitations (e.g. no custom objects in flows, must be published version, global apex classes), overridable templates behavior, and installation failure scenarios.
