---
name: error-recovery-automation-primary
type: execution
version: 2.0.0
description: "Execute deterministic recovery planning for failed automations."
triad:
  lead: "error-recovery-automation-lead"
  support: "error-recovery-automation-support"
  guardian: "error-recovery-automation-guardian"
---

# Error Recovery Automation - Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|-----------|-------------|----------|-----------|
| `{{failure}}` | Failed command, workflow, log excerpt, or incident summary | Yes | User input |
| `{{state_impact}}` | Known state changes, artifacts, migrations, writes, or deployments | Yes | User or repo evidence |
| `{{last_safe_checkpoint}}` | Commit, artifact, backup, checkpoint, or known safe state | No | User or repo evidence |
| `{{constraints}}` | Approval, production, data, compliance, or tool constraints | No | User or guardrails |
| `{{output_format}}` | md or json | No | Auto |

## Execution

1. Load `knowledge/body-of-knowledge.md`.
2. Load assets under `assets/` and apply their policies in this order:
   classification, retry, rollback, escalation, evidence, output contract.
3. Lead: capture failure evidence, classify recoverability, and draft the
   recovery plan.
4. Support: challenge idempotency, destructive side effects, missing evidence,
   rollback feasibility, and validation gaps.
5. Guardian: block delivery if retry is unbounded, evidence is missing,
   rollback is required but absent, or escalation lacks owner and handoff.

## Output

- Failure Summary
- Classification
- Recovery Plan
- Retry Policy or Retry Block
- Rollback Plan
- Escalation Handoff
- Validation Evidence
- Risks And Limits
- Guardian Decision
