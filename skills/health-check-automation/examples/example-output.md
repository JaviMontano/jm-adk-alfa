# Example Output

## Health Surface

- Service: `qa-report-api`. [EXPLICIT]
- Snapshot source: release-candidate captured JSON. [EXPLICIT]
- Required checks: readiness, queue, disk, memory, scheduled job, alert route.
  [EXPLICIT]

## Service Checks

- `readiness`: pass because the captured endpoint status is `200`. [EXPLICIT]
- `scheduled-report-job`: pass because the captured runtime is `48s`, below the
  `120s` warning threshold. [EXPLICIT]

## Dependency Checks

- `queue`: pass because the captured dependency status is `available`.
  [EXPLICIT]

## Resource Checks

- `disk_usage_percent`: pass because `71` is below warning threshold `80` and
  critical threshold `90`. [EXPLICIT]
- `memory_usage_percent`: pass because `63` is below warning threshold `75` and
  critical threshold `90`. [EXPLICIT]

## Alerts

- Severity: `info`. [EXPLICIT]
- Owner: `qa-oncall`. [EXPLICIT]
- Trigger: alert only if a required check becomes `warn` or `fail`. [EXPLICIT]

## Degradation

- Degraded mode is not active because every required check passed with evidence.
  [EXPLICIT]

## Validation Evidence

- Pre-release validation: validate captured JSON with
  `scripts/validate_health_check.py`. [EXPLICIT]
- Post-release validation: rerun readiness and scheduled job checks from the
  release pipeline. [EXPLICIT]

## Guardian Decision

- Status: pass. [EXPLICIT]
- Overall health: `healthy`. [EXPLICIT]
- Remaining risk: live production health still depends on fresh post-release
  evidence. [EXPLICIT]
