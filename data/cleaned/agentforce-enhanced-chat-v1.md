---
id: agentforce-enhanced-chat-v1
title: Connect an Agent to Enhanced Chat v1
source_type: salesforce_help
source_url: https://help.salesforce.com/s/articleView?id=ai.agent_deploy_enhanced_chat_v1.htm&language=en_US&type=5
certification: Agentforce Specialist
exam_domain: AI Agents
product_area: Agentforce Platform
topic: Enhanced Chat v1 Connection
retrieved_date: 2026-06-28
release_relevance: current
authority: official
status: active
---

# Connect an Agent to Enhanced Chat v1

## Summary

Enhanced Chat v1 connects Service agents to messaging interfaces and Employee agents to authenticated users on Experience Cloud sites through inbound Omni-Channel routing.

## Key Concepts

- Enhanced Chat v1
- Enhanced Web Chat v1
- Service agent
- Employee agent
- Inbound Omni-Channel flow
- Route Work
- Messaging channel
- Credential-based user verification
- Logged-in user context
- Embedded service deployment

## Source Content

For a Service agent, create an inbound Omni-Channel flow. In the Route Work action, set the service channel to Messaging, route to the Agentforce Service Agent and its name, and provide a fallback messaging queue.

Add the inbound flow to an Enhanced Chat channel and activate the channel. One agent can connect to multiple inbound channels, but an inbound channel can connect to only one agent. Confirm that the active flow appears under Inbound Routing in the agent’s Messaging connection.

Configure an embedded service deployment to add the Service agent to a messaging interface. The Escalation subagent and an outbound Omni-Channel flow transfer conversations from the agent.

An Employee agent connected to Enhanced Web Chat v1 on an Experience Cloud site runs in the logged-in user’s context. Each user needs the required licenses, permissions, and access to the agent. Unauthenticated users are not supported.

For the Employee agent, add the Experience Cloud domain and inbound flow to the Enhanced Chat channel, turn on credential-based user verification, configure an embedded service deployment, add credential-based user verification to the site, and publish the site.

Avoid routing a conversation to a service rep and an AI agent at the same time.

## Exam Relevance

This source supports the AI Agents objective about digital-experience channels. It distinguishes Service-agent messaging setup from authenticated Employee-agent deployment to Experience Cloud with Enhanced Web Chat v1.

## Notes

Use this source for questions about inbound routing, channel-to-agent cardinality, logged-in user context, credential-based verification, and Enhanced Chat v1 escalation.
