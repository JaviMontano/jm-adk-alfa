---
name: health-check-automation-deep
type: execution
version: 2.0.0
description: "Full health-check design for services with dependencies, resources, jobs, and alerts."
---

# Deep Health Design

Use when the health surface spans multiple services, production dependencies,
resource thresholds, scheduled jobs, or release gates.

## Steps

1. Build the health surface inventory.
2. Bind service, dependency, resource, job, and alert checks to evidence.
3. Apply `assets/service-policy.json`,
   `assets/dependency-policy.json`, and `assets/resource-policy.json`.
4. Apply `assets/alert-policy.json` and `assets/degradation-policy.json`.
5. Produce the output sections in `assets/health-check-contract.json`.
6. For JSON output, validate with `scripts/validate_health_check.py`.

## Output

Return a complete health report with checks, evidence, thresholds, alert
routing, degradation behavior, and Guardian decision.
