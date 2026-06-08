# Health Check Automation - Knowledge Graph

## Core Concepts

- [[health-surface]] defines services, dependencies, resources, jobs, and alert
  routes in scope.
- [[captured-evidence]] provides observed values and snapshot metadata.
- [[deterministic-check]] compares observed values to explicit thresholds.
- [[status-classification]] maps each check to pass, warn, fail, or unknown.
- [[alert-routing]] maps warn and fail outcomes to owner and handoff.
- [[degradation-plan]] defines safe operation when checks are not passing.
- [[guardian-decision]] determines overall healthy, degraded, unhealthy, or
  blocked status.

## Flow

- [[health-surface]] -> [[deterministic-check]]
- [[captured-evidence]] -> [[deterministic-check]]
- [[deterministic-check]] -> [[status-classification]]
- [[status-classification]] -> [[alert-routing]]
- [[status-classification]] -> [[degradation-plan]]
- [[status-classification]] -> [[guardian-decision]]
