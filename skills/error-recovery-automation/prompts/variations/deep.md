---
name: error-recovery-automation-deep
type: execution
version: 2.0.0
description: "Full recovery design for complex or stateful failures."
---

# Deep Recovery Design

Use when the failure may involve production state, partial deployment, data
integrity, credentials, schema drift, or multiple owners.

## Steps

1. Build an evidence table from logs, commands, artifacts, checkpoints, and
   owner-provided constraints.
2. Classify the error with `assets/classification-policy.json`.
3. Decide retry eligibility with `assets/retry-policy.json`.
4. Define rollback and verification with `assets/rollback-policy.json`.
5. Define escalation triggers and handoff with
   `assets/escalation-policy.json`.
6. Produce the output sections in `assets/error-recovery-contract.json`.
7. For JSON output, validate with `scripts/validate_error_recovery.py`.

## Output

Return a full recovery plan with evidence, assumptions, blocked decisions,
validation commands, and residual risks.
