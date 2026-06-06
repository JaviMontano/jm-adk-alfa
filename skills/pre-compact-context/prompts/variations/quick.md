---
name: pre-compact-context-quick
type: variation
version: 2.1.0
description: "Fast P0/P1 preservation before imminent compaction."
---

# Pre Compact Context - Quick Mode

## When To Use

Use quick mode when the context window is close to full and the packet must keep
only critical resume state.

## Execution

1. Read `assets/retention-policy.json`.
2. Preserve P0 hard rules, active objective, branch/PR state, blockers, and next
   action.
3. Compress P1 commands, changed files, assumptions, and decisions.
4. Drop only repeated or stale material with reasons.
5. Emit a short rehydration prompt.

## Output

Do not omit Guardian Decision, Risks And Blockers, or Open Questions.
