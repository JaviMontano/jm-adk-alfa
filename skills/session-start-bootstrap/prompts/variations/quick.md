---
name: session-start-bootstrap-quick
type: variation
version: 2.1.0
description: "Fast startup gate for already-known repos."
---

# Session Start Bootstrap - Quick Mode

## When To Use

Use quick mode when repo and objective are known and the only need is a safe
startup gate.

## Execution

1. Verify branch and dirty-tree state.
2. Check open PR state if workflow requires exclusivity.
3. Load root instructions and the active handoff only.
4. Emit guardrails, blockers, and first action.

## Output

Keep it compact but do not omit Guardian Decision.
