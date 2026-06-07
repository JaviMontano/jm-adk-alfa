---
name: analytics-events-primary
type: execution
version: 2.0.0
description: "Execute the Analytics Events workflow with deterministic tracking plan validation."
triad:
  lead: "analytics-events-lead"
  support: "analytics-events-support"
  guardian: "analytics-events-guardian"
---

# Analytics Events — Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|-----------|-------------|----------|-----------|
| `{{task}}` | Event taxonomy or tracking plan request | Yes | User input |
| `{{context}}` | Product surfaces, journeys, platforms, destinations, privacy constraints, and existing events | Yes | User or codebase |
| `{{constraints}}` | Governance, privacy, naming, or destination rules | No | Guardrails JSON |
| `{{depth}}` | quick / standard / deep | No | Auto |
| `{{output_format}}` | html / docx / xlsx / md | No | Auto |

## Execution

1. Load `knowledge/body-of-knowledge.md` and the contracts in `assets/`.
2. Confirm the task is about analytics events, tracking plan, instrumentation, identity, or event taxonomy.
3. Inventory journeys, surfaces, destinations, current events, privacy constraints, and evidence.
4. Produce taxonomy, events, properties, identity policy, tracking plan, governance, and validation checks.
5. Guardian validates against `assets/analytics-events-contract.json`; structured JSON must pass `scripts/validate_analytics_events.py`.

## Output

- Tracking plan deliverable for `{{task}}` in `{{output_format}}`
- Evidence references for source artifacts, privacy constraints, and validation
- Risks, assumptions, and blocked gaps
- Validation status against naming, properties, identity, tracking plan, privacy, and evidence checks
