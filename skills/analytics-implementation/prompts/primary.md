---
name: analytics-implementation-primary
type: execution
version: 2.0.0
description: "Execute the Analytics Implementation workflow with deterministic GA4/Firebase validation."
triad:
  lead: "analytics-implementation-lead"
  support: "analytics-implementation-support"
  guardian: "analytics-implementation-guardian"
---

# Analytics Implementation — Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|-----------|-------------|----------|-----------|
| `{{task}}` | Analytics implementation outcome | Yes | User input |
| `{{context}}` | Platforms, tools, events, conversions, export, dashboards, privacy, and QA constraints | Yes | User or codebase |
| `{{constraints}}` | Consent, privacy, destination, or rollout rules | No | Guardrails JSON |

## Execution Steps
1. Confirm the request is about GA4, Firebase Analytics, conversions, user properties, BigQuery export, Looker Studio readiness, or analytics QA.
2. Load `assets/analytics-implementation-contract.json` and related policy files.
3. Produce setup, events, conversions, user properties, export, dashboards, implementation steps, and validation checks.
4. If structured JSON is requested, validate with `scripts/validate_analytics_implementation.py`.
