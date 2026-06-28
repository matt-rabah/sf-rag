---
id: agentforce-other-messaging-channels
title: Connect a Service Agent to Other Messaging Channels
source_type: salesforce_help
source_url: https://help.salesforce.com/s/articleView?id=ai.service_agent_messaging.htm&language=en_US
certification: Agentforce Specialist
exam_domain: AI Agents
product_area: Agentforce Platform
topic: Enhanced Messaging Channel Routing
retrieved_date: 2026-06-28
release_relevance: current
authority: official
status: active
---

# Connect a Service Agent to Other Messaging Channels

## Summary

Enhanced messaging channels, including Bring Your Own Channel, use inbound Omni-Channel flows to route conversations to an Agentforce Service agent.

## Key Concepts

- Enhanced messaging
- Bring Your Own Channel
- Agentforce Service agent
- Inbound Omni-Channel flow
- Route Work
- Messaging Session
- Fallback queue
- Inbound Routing
- Outbound routing

## Source Content

Create an inbound Omni-Channel flow that routes messages to the Agentforce Service agent. In the Route Work action, supply the record ID variable, select Messaging as the service channel, select Agentforce Service Agent and the agent’s name as the destination, and provide a fallback messaging queue.

The fallback queue receives the conversation when the inbound flow can’t route it to the agent.

Add the inbound flow to the enhanced messaging channel and activate the channel. An agent can connect to multiple inbound channels, but each inbound channel can connect to only one agent.

Save and commit the agent in Agentforce Builder. In the Messaging connection, confirm that the inbound Omni-Channel flow appears under Inbound Routing. If it is missing, activate the flow and refresh the builder.

Agents on messaging channels use the Escalation subagent and an outbound Omni-Channel flow to transfer conversations. Configure outbound routing after inbound routing.

Do not configure routing procedures that simultaneously route a conversation to a service rep and an AI agent.

## Exam Relevance

This source supports the AI Agents objective about connecting agents to messaging channels beyond Enhanced Chat, including Bring Your Own Channel. It clarifies inbound routing, fallback behavior, and the transition to outbound escalation routing.

## Notes

Use this source for questions about enhanced messaging channel routing, fallback queues, inbound-channel constraints, and when to configure outbound routing.
