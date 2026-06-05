---
name: user-representative-primary
type: execution
version: 2.0.0
description: "Execute the User Representative workflow."
triad:
  lead: "user-representative-lead"
  support: "user-representative-support"
  guardian: "user-representative-guardian"
---

# User Representative — Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|-----------|-------------|----------|-----------|
| `{{task}}` | What to accomplish | Yes | User input |
| `{{context}}` | Background and constraints | Yes | User or codebase |
| `{{constraints}}` | Additional rules | No | Guardrails JSON |

## Execution Steps
1. Read SKILL.md `## When to Activate` and confirm this skill applies.
2. Read SKILL.md `## Deterministic Contract` and `## Validation Gate`.
3. Build the evidence map from provided source facts before scoring.
4. Produce the exact review packet sections from `templates/output.md`.
5. Validate the verdict against the score algorithm before delivering.
