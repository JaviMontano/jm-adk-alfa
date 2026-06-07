---
name: git-workflow-quick
type: variation
version: 2.0.0
description: "Git Workflow in quick mode."
---

# Git Workflow - Quick Mode

## When to Use

Use quick mode for a single Git operation with known repo state.

## Dynamic Parameters

| Parameter | Required | Filled By |
|-----------|----------|-----------|
| `{{task}}` | Yes | User input |
| `{{context}}` | No | Auto-detected |
| `{{depth}}` | No | Set to "quick" |

## Execution

1. Confirm repo state and stop conditions.
2. Produce branch, commit, PR, validation, and cleanup steps.
3. Validate command safety and evidence tags.

## Output

- Compact workflow plan with blockers, commands, validation, and next action.
