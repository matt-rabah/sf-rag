---
id: agentforce-data-masking-limitations
title: Data Masking Limitations in Agentforce
source_type: salesforce_help
source_url: https://help.salesforce.com/s/articleView?id=ai.agent_trust_data_masking.htm&language=en_US&type=5
certification: Agentforce Specialist
exam_domain: Governance & Observability
product_area: Agentforce Platform
topic: Data Masking Limitations
retrieved_date: 2026-06-28
release_relevance: current
authority: official
status: active
---

# Data Masking Limitations in Agentforce

## Summary

Data masking is one Einstein Trust Layer protection used in Agentforce, but it is not the only protection.

Agentforce also relies on broader Trust Layer policies and zero data retention protections when information is sent to an LLM outside the Salesforce trust boundary.

## Key Concepts

- Agentforce
- Einstein Trust Layer
- Data masking
- Data masking limitations
- Sensitive data
- Data misuse
- Data leaks
- Salesforce trust boundary
- LLM provider
- Zero data retention
- Training protection
- Data privacy
- Governance
- Security

## Source Content

Einstein Trust Layer includes several policies and features to help protect sensitive data from misuse or leaks beyond data masking.

Data masking is one Trust Layer protection, but it is not the full security model.

Information sent to an LLM outside of the Salesforce trust boundary is subject to a zero data retention contract with the LLM provider.

Information sent to the LLM is not retained by the provider after the generated response has been sent back to Salesforce.

Information sent to the LLM is not viewed by the provider after the generated response has been sent back to Salesforce.

Information sent to the LLM is not used for training by the provider after the generated response has been sent back to Salesforce.

## Exam Relevance

This source supports the Governance & Observability domain of the Salesforce Certified Agentforce Specialist exam.

It is relevant because the exam expects understanding of Trust Layer security controls, data masking limitations, data privacy, the Salesforce trust boundary, and zero data retention protections for LLM interactions.

## Notes

Use this source for questions about Agentforce data masking limitations, Trust Layer protections beyond masking, zero data retention, LLM provider retention, whether provider data is used for training, and information sent outside the Salesforce trust boundary.
