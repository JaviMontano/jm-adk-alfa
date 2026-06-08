---
name: health-check-automation-quick
type: execution
version: 2.0.0
description: "Fast health-check triage with deterministic gates."
---

# Quick Health Triage

Use when the user needs an immediate healthy, degraded, unhealthy, or blocked
decision from supplied evidence.

## Steps

1. List required checks and supplied evidence.
2. Mark each check pass, warn, fail, or unknown.
3. Block healthy status if any required check is not pass.
4. Require alert owner and trigger for warn or fail outcomes.
5. Record validation evidence and residual risks.

## Output

- Decision
- Blocking checks
- Alert handoff
- Validation check
