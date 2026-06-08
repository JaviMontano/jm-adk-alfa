---
name: quality-metrics-primary
type: execution
version: 2.0.0
description: "Execute the deterministic Quality Metrics workflow."
triad:
  lead: "quality-metrics-lead"
  support: "quality-metrics-support"
  guardian: "quality-metrics-guardian"
---

# Quality Metrics Execute

1. Confirm the request is about metrics, thresholds, coverage, complexity, duplication, Lighthouse, bundle size, or Firestore I/O.
2. Gather available evidence from reports, CI artifacts, user facts, or local read-only inspection.
3. Evaluate the six canonical metrics in `assets/metrics-thresholds.json`.
4. Define gates using `assets/gate-policy.json`.
5. Compute quality score and overall status.
6. Rank top actions using `assets/action-priority-policy.json`.
7. Run Guardian validation before final output.
