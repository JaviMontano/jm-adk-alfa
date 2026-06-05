---
name: quality-gatekeeper-primary
type: execution
version: 2.0.0
description: "Execute the deterministic Quality Gatekeeper workflow."
triad:
  lead: "quality-gatekeeper-lead"
  support: "quality-gatekeeper-support"
  guardian: "quality-gatekeeper-guardian"
---

# Quality Gatekeeper Execute

## Objective

Evaluate one JM-ADK G0-G3 gate decision with explicit criteria, evidence,
blocking, remediation, and score-history entry. [EXPLICIT]

## Required Inputs

- `gate_id` or a clearly inferable gate.
- Current and target stage.
- Evidence sources or explicit missing-evidence statements.
- Prior gate pass records when validating G1-G3.

## Execution Steps

1. Confirm activation using `assets/activation-policy.json`.
2. Load gate criteria, report contract, evidence policy, and score-history
   schema.
3. Enforce sequential gate order.
4. Evaluate all scoped criteria exactly once.
5. Mark missing required evidence as `not_verified`.
6. Block on required `fail` or `not_verified`.
7. Emit a score-history entry contract.
8. Validate JSON reports with the local script when available.
