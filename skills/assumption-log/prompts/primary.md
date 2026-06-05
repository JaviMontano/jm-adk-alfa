---
name: assumption-log-primary
type: execution
version: 2.0.1
description: "Execute the deterministic Assumption Log workflow."
triad:
  lead: "assumption-log-lead"
  support: "assumption-log-support"
  guardian: "assumption-log-guardian"
---

# Assumption Log Execute

## Dynamic Parameters

| Parameter | Description | Required |
|---|---|---|
| `{{scope}}` | Project, decision, or delivery context | Yes |
| `{{claims}}` | Claims, assumptions, risks, or uncertainties to track | Yes |
| `{{evidence}}` | Code, config, docs, decision records, or explicit absence of proof | No |
| `{{existing_log}}` | Prior assumption IDs and statuses to preserve | No |

## Execution Steps

1. Confirm activation with `assets/activation-policy.json`.
2. Load `assets/status-policy.json`, `assets/evidence-policy.json`, and `assets/log-contract.json`.
3. Extract candidate assumptions and normalize each to one testable statement.
4. Preserve existing IDs; assign new IDs as gapless `A-NNN`.
5. Assign status, evidence tag, impact, owner, decision link, and validation action.
6. Detect contradictions and connect them to assumption IDs.
7. Build a validation queue for open high-impact assumptions.
8. Calculate evidence-tag percentages and warning threshold.
9. Validate against the local contract when JSON output is available.
