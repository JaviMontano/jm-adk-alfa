---
name: session-manager-primary
type: execution
version: 2.0.0
description: "Execute the deterministic Session Manager workflow."
triad:
  lead: "session-manager-lead"
  support: "session-manager-support"
  guardian: "session-manager-guardian"
---

# Session Manager — Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|---|---|---:|---|
| `{{task}}` | Session-state task or status request | Yes | User input |
| `{{context}}` | Known repo, feature, and workflow constraints | Yes | User or codebase |
| `{{constraints}}` | Branch, write, or confirmation guardrails | No | Guardrails JSON |

## Execution Steps

1. Confirm activation through `SKILL.md ## When to Activate`.
2. Load `assets/priming-policy.json`, `assets/stage-policy.json`, and
   `assets/persistence-policy.json`.
3. Read `.specify/context.json`, latest plan, active tasks, and feature tests in
   the policy order.
4. Compute the current stage from artifact evidence.
5. Block any stage skip, missing-context pass, or unauthorized write.
6. Return the status report using `templates/output.md`.
7. When a machine report is produced, validate it with
   `scripts/validate_session_manager_report.py`.
