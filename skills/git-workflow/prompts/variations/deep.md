---
name: git-workflow-deep
type: variation
version: 2.0.0
description: "Git Workflow — deep analysis mode. Exhaustive coverage."
---

# Git Workflow - Deep Mode

## When to Use

Use deep mode for release tagging, conflict recovery, protected branch policy, multi-PR sequencing, or CI-sensitive changes.

## Dynamic Parameters

| Parameter | Required | Filled By |
|-----------|----------|-----------|
| `{{task}}` | Yes | User input |
| `{{context}}` | Yes | User + codebase scan |
| `{{depth}}` | No | Set to "deep" |

## Execution (Deep)

1. Inspect workflow docs, CI config, PR templates, release notes, and branch protection hints.
2. Build a complete command plan with preconditions and rollback notes.
3. Include conflict resolution, failed-CI handling, release-tag verification, and branch cleanup.
4. Guardian validates command safety and stop conditions before any execution recommendation.

## Output

- Full workflow plan with evidence trail, edge cases, risk assessment, and merge/release criteria.
