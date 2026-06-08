---
name: quality-engineering-primary
type: execution
version: 2.0.0
description: "Execute the deterministic Quality Engineering workflow."
triad:
  lead: "quality-engineering-lead"
  support: "quality-engineering-support"
  guardian: "quality-engineering-guardian"
---

# Quality Engineering Execute

1. Confirm the request is about quality strategy, gates, automation architecture, shift-left practice, maturity, or metrics.
2. Gather available evidence with read-only inspection or user-provided facts.
3. Score the six dimensions in `assets/maturity-model.json`.
4. Select the architecture-specific test shape from `assets/test-strategy-policy.json`.
5. Define canonical gates from `assets/gate-policy.json`.
6. Include required metrics from `assets/metrics-policy.json`.
7. Rank top actions using `assets/action-priority-policy.json`.
8. Run Guardian validation before final output.
