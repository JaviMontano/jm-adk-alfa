---
name: ux-writing-primary
type: execution
version: 2.0.0
description: "Execute the Ux Writing workflow."
triad:
  lead: "ux-writing-lead"
  support: "ux-writing-support"
  guardian: "ux-writing-guardian"
---

# UX Writing — Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|-----------|-------------|----------|-----------|
| `{{task}}` | What to accomplish | Yes | User input |
| `{{context}}` | Background and constraints | Yes | User or codebase |
| `{{constraints}}` | Additional rules | No | Guardrails JSON |

## Execution Steps
1. Read SKILL.md `## When to Activate` and confirm this skill applies.
2. Read SKILL.md `## Deterministic Contract` and `## Validation Gate`.
3. Extract source copy and constraints before proposing rewrites.
4. Produce the exact packet sections from `templates/output.md`.
5. Validate the packet against the local contract before delivering when a Markdown packet is produced.
