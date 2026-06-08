# Health Check Automation - Body of Knowledge

## Canon

Health automation must prove status from scoped checks and captured evidence.
An endpoint returning success is not enough when dependencies, jobs, resources,
or alert routes are missing. Required checks with `fail`, `warn`, `unknown`, or
stale evidence prevent an unqualified healthy decision.

## Status Model

| Status | Meaning | Overall Impact |
|--------|---------|----------------|
| `pass` | Check meets policy with evidence | Eligible for healthy |
| `warn` | Check breaches warning policy | Degraded or at risk |
| `fail` | Check breaches critical policy | Unhealthy |
| `unknown` | Evidence missing, stale, or unavailable | Blocks healthy |

## Health Surfaces

- Service readiness and liveness.
- Required dependencies such as databases, queues, caches, APIs, and storage.
- Resource usage such as CPU, memory, disk, queue depth, and error rate.
- Scheduled or batch jobs.
- Alert routing and owner handoff.
- Degraded mode and recovery expectations.

## Quality Metrics

| Metric | Target | How to Measure |
|--------|--------|---------------|
| Required check coverage | 100% | Every required check appears in the report |
| Evidence coverage | 100% | Every check references captured evidence |
| Threshold determinism | 100% | Resource checks include unit, warning, critical, and observed values |
| Alert readiness | 100% | Warn/fail outcomes identify severity, owner, trigger, and handoff |
| Healthy decision safety | 100% | Overall healthy requires all required checks to pass |

## References

- `assets/health-check-contract.json`
- `assets/service-policy.json`
- `assets/dependency-policy.json`
- `assets/resource-policy.json`
- `assets/alert-policy.json`
- `assets/degradation-policy.json`
- `assets/evidence-policy.json`
- `scripts/validate_health_check.py`
