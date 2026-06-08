# Health Check Automation Assets

These assets define the deterministic contract for health-check reports.

## Files

- `health-check-contract.json`: required report sections and JSON fields.
- `service-policy.json`: service and job status rules.
- `dependency-policy.json`: dependency status and required ownership.
- `resource-policy.json`: resource units, warning thresholds, and critical
  thresholds.
- `alert-policy.json`: alert severity, owner, trigger, and handoff rules.
- `degradation-policy.json`: degraded, unhealthy, and blocked behavior.
- `evidence-policy.json`: evidence freshness and validation requirements.

Use assets as the source of truth before editing prompts or examples.
