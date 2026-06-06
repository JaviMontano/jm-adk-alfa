---
name: changelog-management-primary
type: execution
version: 2.0.0
description: "Execute deterministic Changelog Management workflow."
triad:
  lead: "changelog-management-lead"
  support: "changelog-management-support"
  guardian: "changelog-management-guardian"
---

# Changelog Management — Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|---|---|---:|---|
| `{{task}}` | Requested changelog operation | Yes | User input |
| `{{context}}` | Existing changelog and evidence refs | Yes | Codebase |
| `{{as_of_date}}` | Date for entry placement | Yes | Session config or user |
| `{{constraints}}` | Write authorization and branch rules | No | Guardrails JSON |

## Execution

1. Confirm activation through `SKILL.md ## When to Activate`.
2. Load entry type, ordering, duplicate, and evidence policies from `assets/`.
3. Read `changelog.md` and recent entries.
4. Classify the event, draft entry, and attach rationale, principles, and evidence.
5. Run duplicate review and ordering review.
6. Block unsupported types, future dates, duplicate append, missing evidence, or
   unauthorized writes.
7. Return the Markdown report using `templates/output.md`.
8. When a JSON report is produced, validate it with
   `scripts/validate_changelog_report.py`.
