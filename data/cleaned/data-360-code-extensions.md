---
id: data-360-code-extensions
title: Code Extensions in Data 360
source_type: salesforce_help
source_url: data_360_6-28-2026.pdf
certification: Agentforce Specialist
exam_domain: Data 360 Fundamentals
product_area: Data 360
topic: Chunking
retrieved_date: 2026-06-28
release_relevance: current
authority: official
status: active
---

# Code Extensions in Data 360

## Summary

Code extensions allow developers to bring custom Python code into Data 360 to extend native capabilities. Custom Python code runs as scripts (for batch transforms) or functions (for search index chunking).

## Key Concepts

- Code Extension
- Custom Script
- Custom Function
- Code Extension Toolchain
- Compute Size Impact on Billing
- Custom Function Standby Time
- Custom Function System Limit

## Source Content

**Code Extension Overview**
Bring your custom Python code into Data 360 to extend Data 360's native capabilities by using code extension. If the native Data 360 features don't meet your business requirements, deploy your custom logic to supported Data 360 features.

Code extension supports two types of custom code, which differ in how they run:
- **Scripts:** Run as a batch data transform—a job that you run on demand or schedule.
- **Functions:** Run as part of the search index pipeline, where they control how content is chunked for search and AI retrieval.

**Code Extension Workflow**
The workflow involves collaboration between developers and users with a Data Cloud Architect permission set:
1. Developers author and validate custom Python code locally using Salesforce CLI with the Code Extension plugin and the Data Custom Code Python SDK as the toolchain.
2. In a sandbox, users upload custom code packages and use the custom code in the relevant feature—a batch data transform for a script, or a search index for a function—and run it.
3. After validation, they package the custom code and dependencies into a data kit.
4. In production, they install the data kit, run the custom code, and monitor execution.

**Compute Size Impact on Billing**
The compute size selected for custom code deployment directly affects credit consumption. The available compute size options are:
- Standard - Large: 4 Compute Units per hour
- Standard - X-Large: 8 Compute Units per hour
- Standard - 2X-Large: 16 Compute Units per hour
- Standard - 4X-Large: 32 Compute Units per hour

**Standby Time and Limits**
- **Standby Time:** Code extension chunking functions incur compute charges while active, including 1 hour of standby time after execution completes. If a new request arrives during the standby period, the 1-hour standby timer resets. This keeps the function warm for faster search index processing.
- **System Limit:** The maximum runtime (duration) of a custom function before it is canceled by the system limit of 5 minutes.

## Exam Relevance

This source supports the Data 360 Fundamentals domain of the Agentforce Specialist exam by detailing Code Extensions, custom chunking functions in search index configurations, compute size options, standby billing rules, and the 5-minute custom function execution limit.
