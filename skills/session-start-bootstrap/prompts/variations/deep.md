---
name: session-start-bootstrap-deep
type: variation
version: 2.1.0
description: "Deep startup for complex repos, stale handoffs, and strict workflows."
---

# Session Start Bootstrap - Deep Mode

## When To Use

Use deep mode when the repo has multiple instruction layers, stashes, open PR
risk, stale handoffs, or strict serial workflow rules.

## Execution

1. Read all assets in `assets/`.
2. Verify repo identity, branch, status, open PRs, baseline SHA, stashes, and
   local blockers.
3. Load only relevant instruction, handoff, tasklog, and review sources.
4. Resolve conflicting instructions by source precedence.
5. Emit a startup packet with explicit pass/block decision.

## Output

Include exact commands and paths needed to reproduce startup state.
