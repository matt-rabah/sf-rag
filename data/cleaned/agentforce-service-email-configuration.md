---
id: agentforce-service-email-configuration
title: Create an Email Configuration for Agentforce Service Agent on Email
source_type: salesforce_help
source_url: https://help.salesforce.com/s/articleView?id=ai.service_agent_email_configuration.htm&language=en_US&type=5
certification: Agentforce Specialist
exam_domain: AI Agents
product_area: Agentforce Platform
topic: Agentforce Service Email Channel
retrieved_date: 2026-06-28
release_relevance: current
authority: official
status: active
---

# Create an Email Configuration for Agentforce Service Agent on Email

## Summary

An Agentforce Service Agent email configuration connects an email template and an active Service agent to one or more Email-to-Case routing addresses.

## Key Concepts

- Agentforce Service Agent on Email
- Service Email Connection
- Email configuration
- Email template
- Email-to-Case
- Routing address
- Legal disclosure
- Reply All

## Source Content

First set up the Service Email Connection used to deploy the Agentforce Service agent to email.

In Setup, search for Agentforce and select Agentforce for Service on Email. Create a new configuration, provide a name, select the email template, and select an active Agentforce Service agent.

Enter a legal disclosure that informs the end user that the email was written and sent by AI. Salesforce inserts this disclosure into the sent email. Optionally enable Reply All for responses to recipients in the To and CC fields, and then save the configuration.

Continue to Email-to-Case Setup. In Routing Addresses, edit the address that receives inbound email for the Service agent. Under Agentforce Service Agent Settings, select the email configuration and save the routing address.

The same email configuration can be linked to additional routing addresses.

## Exam Relevance

This source supports the AI Agents objective about connecting agents to email. It describes the relationship among the Service Email Connection, email template, active agent, email configuration, and Email-to-Case routing address.

## Notes

Use this source for questions about creating the email configuration, providing the AI legal disclosure, and linking inbound routing addresses to an Agentforce Service agent.
