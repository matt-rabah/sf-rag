---
id: agentforce-transfer-conversations-omni-channel
title: Transfer Conversations from an Agent with an Omni-Channel Flow
source_type: salesforce_help
source_url: https://help.salesforce.com/s/articleView?id=ai.service_agent_escalation.htm&language=en_US
certification: Agentforce Specialist
exam_domain: AI Agents
product_area: Agentforce Platform
topic: Agent Conversation Escalation
retrieved_date: 2026-06-28
release_relevance: current
authority: official
status: active
---

# Transfer Conversations from an Agent with an Omni-Channel Flow

## Summary

When an agent can’t resolve a conversation, the Escalation subagent can use an outbound Omni-Channel flow to transfer the session, its history, and gathered information to another destination.

## Key Concepts

- Escalation subagent
- Outbound Omni-Channel flow
- Service representative
- Queue
- Different agent
- Conversation history
- Escalation message
- Transfer testing
- Check Availability for Routing

## Source Content

An Agentforce Service agent or Employee agent needs the Escalation subagent to escalate sessions. Customize the subagent’s actions and instructions so escalation follows company policy.

For enhanced messaging channels, a Service agent transfers conversations to a service rep, queue, different agent, or other destination through an outbound Omni-Channel flow. The transfer includes conversation messages and information gathered before escalation.

Create and activate the outbound Omni-Channel flow. In the new Agentforce Builder, open the Messaging connection and select the flow in the Escalation Flow field. Add an escalation message that clearly tells the customer that the conversation is being transferred.

Test escalation by activating the agent and chatting on a connected channel. Escalation can’t be tested in Agentforce Builder because a builder conversation has no Messaging Session record.

If a transfer can’t be completed, the agent continues the session using the Escalation subagent and retains the earlier context. The agent attempts transfer with the Escalation subagent only once per session.

The outbound flow can use Check Availability for Routing to determine representative availability and estimated wait time before routing.

## Exam Relevance

This source supports the AI Agents objective about channel handoff and human escalation. It describes the required subagent, outbound flow, transfer destinations, preserved context, user-facing message, and channel-based testing.

## Notes

Use this source for questions about outbound escalation setup, what transfers with a conversation, testing constraints, and behavior when a transfer fails.
