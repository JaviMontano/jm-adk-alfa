---
name: error-recovery-automation-quick
type: execution
version: 2.0.0
description: "Fast recovery triage with deterministic safety gates."
---

# Quick Recovery Triage

Use when the user needs an immediate go/no-go decision.

## Steps

1. Identify failed command, error excerpt, and state impact.
2. Classify as retryable, blocked, or human-required.
3. Allow retry only when attempts, max delay, idempotency, and stop conditions
   are explicit.
4. Require rollback before retry when state changed.
5. Escalate when evidence is missing or retry is unsafe.

## Output

- Decision: retry, block, or escalate
- Evidence used
- Required next command or handoff
- Validation check
