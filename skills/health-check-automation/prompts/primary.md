---
name: health-check-automation-primary
type: execution
version: 2.0.0
description: "Execute deterministic health-check planning and report validation."
triad:
  lead: "health-check-automation-lead"
  support: "health-check-automation-support"
  guardian: "health-check-automation-guardian"
---

# Health Check Automation - Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|-----------|-------------|----------|-----------|
| `{{health_surface}}` | Services, dependencies, resources, jobs, and alert routes | Yes | User or repo evidence |
| `{{snapshot}}` | Captured values, timestamp, and source labels | Yes | User or fixture |
| `{{thresholds}}` | Warning and critical thresholds | No | Assets or user input |
| `{{constraints}}` | Release, production, ownership, or alerting constraints | No | User or policy |
| `{{output_format}}` | md or json | No | Auto |

## Execution

1. Load `knowledge/body-of-knowledge.md`.
2. Load assets under `assets/` and apply policies in this order: contract,
   service, dependency, resource, alert, degradation, evidence.
3. Lead: inventory health surface, bind checks to evidence, and draft report.
4. Support: challenge missing thresholds, stale snapshots, unknown required
   checks, alert owner gaps, and false healthy decisions.
5. Guardian: block healthy status when any required check is warn, fail,
   unknown, stale, or missing evidence.

## Output

- Health Surface
- Service Checks
- Dependency Checks
- Resource Checks
- Alerts
- Degradation
- Validation Evidence
- Risks And Limits
- Guardian Decision
