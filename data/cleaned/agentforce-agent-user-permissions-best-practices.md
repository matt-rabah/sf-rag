---
id: agentforce-agent-user-permissions-best-practices
title: Best Practices for Agent User Permissions
source_type: salesforce_help
source_url: https://help.salesforce.com/s/articleView?id=ai.agent_user.htm&language=en_US&type=5
certification: Agentforce Specialist
exam_domain: AI Agents
product_area: Agentforce Platform
topic: Agent User Permissions
retrieved_date: 2026-06-28
release_relevance: current
authority: official
status: active
---

# Best Practices for Agent User Permissions

## Summary

Agent user permissions control what an Agentforce agent can securely access and do.

The agent user permission model helps make sure an agent has the access it needs for its job without granting unnecessary access.

## Key Concepts

- Agentforce
- Agent user
- Agent user permissions
- Salesforce integration user
- Secure access
- Data access
- Action access
- Permission sets
- Least privilege
- Agent security
- Governance
- Access control

## Source Content

Agent user permissions determine what data and functionality an agent can access while performing work.

Service agents operate as an agent user, which is a Salesforce integration user with the permissions the agent needs to do its job.

Agent user permissions should be configured so the agent has access to the data and actions required for its assigned use case.

Avoid granting unnecessary access to the agent user.

Use permission sets and access controls to align the agent user's access with the agent's intended work.

Agent user permission design is part of securing Agentforce agents before deployment.

## Exam Relevance

This source supports the AI Agents domain and the Governance & Observability domain of the Salesforce Certified Agentforce Specialist exam.

It is relevant because the exam requires understanding how agents securely access data, perform actions, and follow permissions while operating in Salesforce.

## Notes

Use this source for questions about agent users, integration users, permissions, least privilege, data access, action access, and secure Agentforce configuration.
