---
name: find-skills-primary
type: execution
version: 2.0.0
description: "Execute the Find Skills workflow."
triad:
  lead: "find-skills-lead"
  support: "find-skills-support"
  guardian: "find-skills-guardian"
---

# Find Skills — Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|-----------|-------------|----------|-----------|
| `{{query}}` | Capability or task to find a skill for | Yes | User input |
| `{{scope}}` | `local-only`, `remote-only`, or `all` | No | User or default |
| `{{constraints}}` | Offline, security, installation, or source limits | No | User or guardrails |

## Execution Steps

1. Parse domain, task, scope, and installation intent.
2. Read `assets/source-policy.json`, `assets/scoring-rubric.json`, `assets/install-policy.json`, and `assets/report-contract.json`.
3. Search local catalogs first unless scope is `remote-only`.
4. Search remote sources only when scope allows and execution context permits network.
5. Score every candidate and cap default output at 5 candidates.
6. Reject Tier F and unscored candidates.
7. Present install commands only; do not run them without explicit confirmation.
8. Validate JSON reports with `scripts/validate_find_skills_report.py` when a report artifact is produced.
