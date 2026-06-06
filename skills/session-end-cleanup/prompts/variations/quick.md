---
name: session-end-cleanup-quick
type: variation
version: 2.1.0
description: "Fast closeout for low-risk sessions with stable evidence."
---

# Session End Cleanup - Quick Mode

## When To Use

Use quick mode when the session is small, the evidence is already available, and
there are no failed validations or ambiguous durable-log writes.

## Execution

1. Read `assets/output-contract.json`.
2. Inventory changed files, commands run, blockers, and next action.
3. Emit the fixed Markdown sections with concise bullets.
4. Block completion if validation, PR, CI, or merge status is unknown but needed
   for the user's requested claim.

## Output

Keep the handoff compact. Do not omit Risks And Blockers or Guardian Decision.
