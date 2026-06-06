---
name: tasklog-management-primary
type: execution
version: 2.0.0
description: "Execute deterministic Tasklog Management workflow."
triad:
  lead: "tasklog-management-lead"
  support: "tasklog-management-support"
  guardian: "tasklog-management-guardian"
---

# Tasklog Management — Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|---|---|---:|---|
| `{{task}}` | Requested tasklog operation | Yes | User input |
| `{{context}}` | Existing tasklog and bridge evidence | Yes | Codebase |
| `{{as_of_date}}` | Date for stale/archive calculations | Yes | Session config or user |
| `{{constraints}}` | Write authorization and branch rules | No | Guardrails JSON |

## Execution

1. Confirm activation through `SKILL.md ## When to Activate`.
2. Load `assets/tasklog-contract.json`, `assets/status-policy.json`,
   `assets/staleness-policy.json`, and `assets/bridge-policy.json`.
3. Read `tasklog.md` and relevant `workspace/tasks/**` bridge paths.
4. Validate IDs, statuses, dates, transitions, stale status, archive eligibility,
   and bridge paths.
5. Block any unauthorized write or hidden-clock decision.
6. Return the Markdown report using `templates/output.md`.
7. When a JSON report is produced, validate it with
   `scripts/validate_tasklog_report.py`.
