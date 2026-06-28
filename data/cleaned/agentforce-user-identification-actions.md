---
id: agentforce-user-identification-actions
title: Add User Identification to Agentforce Actions
source_type: salesforce_help
source_url: https://help.salesforce.com/s/articleView?id=service.service_agentforce_implement_agents.htm&language=en_US&type=5
certification: Agentforce Specialist
exam_domain: AI Agents
product_area: Agentforce Platform
topic: Customer Channel User Identification
retrieved_date: 2026-06-28
release_relevance: current
authority: official
status: active
---

# Add User Identification to Agentforce Actions

## Summary

Agentforce Service agents on customer channels require an identification design that lets private actions confirm who the user is and limit access to that user’s data.

## Key Concepts

- User identification
- Private actions
- Enhanced Chat
- AuthSession
- MessagingSession
- MessagingEndUser
- User Verification
- Experience Cloud authentication
- Third-party messaging
- Session ID

## Source Content

For an Enhanced Chat channel on an Experience site restricted to authenticated users, each messaging session has an active authenticated AuthSession. The user’s Account and Contact IDs are known. Private actions should confirm that those identifiers are assigned and the AuthSession is still active.

For an external site or app with its own authentication, map the Agentforce messaging session to a MessagingSession record. User Verification can securely pass a user identifier to the MessagingEndUser record.

This external-site method does not automatically track an AuthSession. Authentication remains valid until the expiration time in the token, so expiration must follow company standards.

For an enhanced third-party messaging channel, authentication can use channel identifiers, a separate side channel, or authentication messaging components. Delegating authentication to a channel provider requires careful risk review.

After identity confirmation, private actions can use the Session ID and the associated Account and Contact IDs to limit the action to the authenticated user’s data.

## Exam Relevance

This source supports the AI Agents objective about securely connecting agents to customer channels. It distinguishes authenticated Experience Cloud sessions, external Enhanced Chat user verification, and authentication patterns for third-party messaging.

## Notes

Use this source for questions about AuthSession behavior, MessagingSession mapping, User Verification, third-party channel authentication, and scoping private actions.
