---
name: generate-qa-report-primary
type: execution
version: 2.0.0
description: "Execute the Generate Qa Report workflow."
triad:
  lead: "generate-qa-report-lead"
  support: "generate-qa-report-support"
  guardian: "generate-qa-report-guardian"
---

# Generate QA Report - Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|-----------|-------------|----------|-----------|
| `{{task}}` | What to accomplish | Yes | User input |
| `{{context}}` | Background and constraints | Yes | User or codebase |
| `{{constraints}}` | Additional rules | No | Guardrails JSON |

## Execution Steps
1. Confirm the user wants an aggregated QA report, not a new audit run.
2. Read available validation/audit outputs and record source coverage.
3. Normalize findings into severity, category, component, description, recommendation, and evidence.
4. Reconcile summary counts with the normalized findings list.
5. Produce exactly three TL;DR lines and ranked recommendations.
6. Validate against `assets/report-contract.json` before delivery.
