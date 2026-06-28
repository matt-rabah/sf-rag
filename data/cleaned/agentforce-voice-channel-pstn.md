---
id: agentforce-voice-channel-pstn
title: Create the Channel for Agentforce Voice with PSTN
source_type: salesforce_help
source_url: https://help.salesforce.com/s/articleView?id=ai.agent_voice_channel.htm&language=en_US&type=5
certification: Agentforce Specialist
exam_domain: AI Agents
product_area: Agentforce Platform
topic: Agentforce Voice Channel
retrieved_date: 2026-06-28
release_relevance: current
authority: official
status: active
---

# Create the Channel for Agentforce Voice with PSTN

## Summary

An Agentforce Voice messaging channel maps a provisioned PSTN phone number to the inbound Omni-Channel flow that routes transferred calls to the voice-enabled agent.

## Key Concepts

- Agentforce Voice
- PSTN phone number
- Messaging channel
- Inbound calls
- Omni-Channel flow
- Call routing
- Public key
- Channel activation

## Source Content

From Setup, open Agentforce Voice Setup. In the Messaging Channel for Agentforce Voice step, add a channel and enter its name and developer name.

Choose Use a phone number and select the provisioned PSTN number. Only phone numbers with Live status are available, each number can be associated with only one channel, and the number must be provisioned from Agentforce Voice Setup.

Under Call Routing, select the inbound Omni-Channel flow that routes calls to the agent. Use the flow created for inbound call transfers, not the escalation flow, and then save the channel.

For customers who are not using Salesforce Voice with Telephony Providers, edit the channel and provide an unexpired certificate in the Public Key field. Without the public key, Omni-Channel does not route calls to the voice-enabled agent.

Activate the channel. If the agent is deactivated, it does not answer calls to the provisioned number.

## Exam Relevance

This source supports the AI Agents objective about connecting an agent to voice. It covers phone-number mapping, inbound Omni-Channel routing, the public-key condition, and channel activation.

## Notes

Use this source for questions about PSTN Agentforce Voice channel setup, inbound call routing, supported phone numbers, and activation.
