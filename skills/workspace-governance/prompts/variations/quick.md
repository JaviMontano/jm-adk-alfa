---
name: workspace-governance-quick
type: variation
version: 2.0.0
description: "Workspace Governance in quick mode."
---

# Workspace Governance — quick Mode

## When to Use

Use quick mode for a single session folder, `.gitignore` check, or one task bridge.

## Dynamic Parameters

| Parameter | Required | Filled By |
|-----------|----------|-----------|
| `{{task}}` | Yes | User input |
| `{{context}}` | No | Auto-detected |
| `{{depth}}` | No | Set to "quick" |

## Execution

1. Check `.gitignore`.
2. Validate the requested workspace path and README.
3. Confirm session or task bridge naming.
4. Emit safe action plan and Guardian decision.

## Output

- Minimal governance report
- Evidence-tagged safe action
- Guardian pass/block
