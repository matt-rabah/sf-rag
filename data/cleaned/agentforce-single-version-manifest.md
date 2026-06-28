---
id: agentforce-single-version-manifest
title: Manifest Defining a Single Agent Version
source_type: developer_docs
source_url: https://developer.salesforce.com/docs/ai/agentforce/guide/package-singleagent.html
certification: Agentforce Specialist
exam_domain: Testing, Deployment, & Maintenance
product_area: Agentforce Platform
topic: Single Agent Version Deployment
retrieved_date: 2026-06-28
release_relevance: current
authority: official
status: active
---

# Manifest Defining a Single Agent Version

## Summary

A `package.xml` manifest for a single Agentforce version must identify that version and its dependent flows, prompt templates, Apex classes, and other required metadata.

## Key Concepts

- package.xml
- Single agent version
- Full agent deployment
- BotVersion
- AiAuthoringBundle
- GenAiPlannerBundle
- Flows
- Prompt templates
- Apex classes
- Target org dependencies

## Source Content

A single-version manifest defines the metadata for one specific version of an Agentforce agent. It also defines the flows, prompt templates, Apex classes, and other assets used by that version.

Before deploying a single agent version with `BotVersion`, deploy the full agent to the target org. Deploying the full agent first creates the required metadata and artifacts in the target org.

After the full agent exists, deploy the selected version and its matching metadata components. Use the correct versioned names for `BotVersion`, `AiAuthoringBundle`, and `GenAiPlannerBundle`.

If saved `AiAuthoringBundle` versions and committed `BotVersion` versions use different numbers, identify the matching target version from the authoring bundle metadata rather than assuming that the version numbers are equal.

## Exam Relevance

This source supports the Testing, Deployment, & Maintenance objective about deployment sequencing and version-specific dependencies when promoting agents between environments.

## Notes

Use this source for questions about why the full agent precedes a single-version deployment, what dependencies belong in the manifest, and how to match authoring and committed versions.
