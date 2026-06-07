---
name: analytics-engineering-primary
type: execution
version: 2.0.0
description: "Execute the Analytics Engineering workflow."
triad:
  lead: "analytics-engineering-lead"
  support: "analytics-engineering-support"
  guardian: "analytics-engineering-guardian"
---

# Analytics Engineering — Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|-----------|-------------|----------|-----------|
| `{{task}}` | Analytics engineering outcome to design | Yes | User input |
| `{{context}}` | Source systems, warehouse, transformation framework, owners, SLAs, and constraints | Yes | User or codebase |
| `{{constraints}}` | Required governance, privacy, cost, freshness, or CI rules | No | Guardrails JSON |

## Execution Steps
1. Confirm the request is about transformation modeling, source-to-target mapping, materialization strategy, tests, contracts, or lineage.
2. Load `assets/analytics-engineering-contract.json`, `assets/layer-policy.json`, `assets/materialization-policy.json`, `assets/testing-policy.json`, and `assets/data-contract-policy.json`.
3. Inventory sources, owners, freshness, and evidence. Mark unknowns instead of inventing them.
4. Produce model layers with names, grain, owner, materialization, upstream dependencies, tests, contracts, documentation, and validation checks.
5. Validate the output against `## Validation Gate`; if structured JSON is requested, validate with `scripts/validate_analytics_engineering.py`.
