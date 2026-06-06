---
name: pre-compact-context-deep
type: variation
version: 2.1.0
description: "Deep preservation for long sessions, PR lifecycle work, and high-risk handoff."
---

# Pre Compact Context - Deep Mode

## When To Use

Use deep mode when compaction could lose PR lifecycle state, validation results,
multi-step task order, user constraints, or unresolved blockers.

## Execution

1. Read all assets in `assets/`.
2. Inspect git status, branch, PR/CI evidence, changed files, review docs,
   tasklogs, and command outputs needed to resume.
3. Build a source-backed P0/P1/P2/DROP map.
4. Preserve conflicts and source gaps explicitly.
5. Validate that the rehydration prompt includes repo, branch, first command,
   first decision, and first blocker.

## Output

Return the full packet and include enough exact source paths for a clean-session
agent to resume without hidden memory.
