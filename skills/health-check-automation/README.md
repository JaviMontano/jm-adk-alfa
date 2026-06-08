# Health Check Automation

Deterministic health-check planning for services, dependencies, resource usage,
scheduled jobs, alert routing, and degraded operation.

## Triggers

- `health-check-automation`
- `health check automation`
- `health check plan`
- `dependency status`
- `resource usage alerts`
- `service health snapshot`

## Allowed Tools

- Read
- Write
- Glob
- Grep
- Bash

## Quick Use

Use this skill when a system needs health checks that can be reviewed offline.
The skill turns a service inventory and captured evidence into pass, warn, fail,
or unknown decisions with alert and degradation handling.

## Output Format

Markdown or JSON with:

- health surface
- service checks
- dependency checks
- resource checks
- alert routing
- degradation behavior
- validation evidence
- Guardian decision

Structured JSON reports can be validated offline with
`scripts/validate_health_check.py`.
