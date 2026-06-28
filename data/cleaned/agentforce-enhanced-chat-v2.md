---
id: agentforce-enhanced-chat-v2
title: Connect a Service Agent to Enhanced Chat v2
source_type: salesforce_help
source_url: https://help.salesforce.com/s/articleView?id=ai.service_agent_deploy_enhanced_chat_v2.htm&language=en_US&type=5
certification: Agentforce Specialist
exam_domain: AI Agents
product_area: Agentforce Platform
topic: Enhanced Chat v2 Connection
retrieved_date: 2026-06-28
release_relevance: current
authority: official
status: active
---

# Connect a Service Agent to Enhanced Chat v2

## Summary

In the new Agentforce Builder, the Enhanced Chat v2 connection creates the messaging channel and embedded deployment used to route web conversations to an Agentforce Service agent.

## Key Concepts

- Enhanced Chat v2
- Agentforce Service agent
- Agentforce Builder
- Connection routing
- Escalation flow
- Escalation message
- Fallback queue
- Embedded Service deployment
- Unauthenticated and guest users

## Source Content

Enhanced Chat v2 applies to Agentforce Service agents, not Agentforce Employee agents. It currently supports unauthenticated users on external websites and guest users on Salesforce sites. User authentication is not yet supported.

In Agentforce Studio, open the Service agent. From the Explorer panel, add the Enhanced Chat v2 connection and then activate and commit the agent version.

Open Routing under the Enhanced Chat v2 connection. To support escalation to a human service rep, specify an escalation flow and an escalation message.

Create a channel with a name, unique developer name, website domain, and fallback queue. The fallback queue receives work if the agent is unavailable or can’t connect, and the queue must support the Messaging Session object.

Agentforce Builder creates the messaging channel and embedded deployment. Test Enhanced Web Chat from the Embedded Service Deployment settings, publish the site, and add Enhanced Chat v2 to the external website or Salesforce site.

Avoid routing procedures that route the same conversation to a service rep and an AI agent at the same time.

## Exam Relevance

This source supports the AI Agents objective about connecting agents to digital channels. It covers the new-builder workflow, routing and fallback settings, escalation, deployment, and the current authentication limitation for Enhanced Chat v2.

## Notes

Use this source for questions about Enhanced Chat v2 setup, supported agent and user types, fallback queues, and human escalation configuration.
