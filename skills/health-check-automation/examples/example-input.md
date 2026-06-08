# Example Input

Create a deterministic health-check report for the QA report service.

- Service: `qa-report-api`
- Snapshot source: local captured JSON from the release candidate
- Required checks: HTTP readiness, queue dependency, disk usage, memory usage,
  scheduled report job, and alert route
- Observed values:
  - readiness endpoint returned `200`
  - queue status is `available`
  - disk usage is `71%`
  - memory usage is `63%`
  - scheduled report job completed in `48s`
  - alert route owner is `qa-oncall`
- Desired outcome: decide whether the service can be marked healthy and list
  validation evidence
