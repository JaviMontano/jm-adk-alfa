---
name: workspace-governance-deep
type: variation
version: 2.0.0
description: "Workspace Governance — deep analysis mode. Exhaustive coverage."
---

# Workspace Governance — Deep Mode

## When to Use

Use deep mode when scaffolding or auditing a full workspace tree with sessions,
tasks, estandares, stale folders, and `.gitignore` evidence.

## Dynamic Parameters

| Parameter | Required | Filled By |
|-----------|----------|-----------|
| `{{task}}` | Yes | User input |
| `{{context}}` | Yes | User + codebase scan |
| `{{depth}}` | No | Set to "deep" |

## Execution (Deep)

1. Inventory workspace root, task bridges, sessions, estandares, and README coverage.
2. Compare task bridges to open tasklog IDs.
3. Flag sessions older than 30 days for review.
4. Validate proposed actions against path safety.
5. Validate JSON report with `scripts/check.sh`.

## Output

- Full governance report with evidence
- Safe action plan
- Stale-session review list
- Guardian validation
