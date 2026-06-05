---
name: code-review-quick
type: variation
version: 2.1.0
description: "Fast deterministic Code Review for narrow diffs."
---

# Code Review - Quick Mode

## When To Use

Use quick mode for small diffs where the user needs a fast approval risk check.

## Execution

1. Confirm code artifact and scope.
2. Inspect changed lines and directly adjacent context.
3. Report only `BLOCKER`, `MAJOR`, and high-signal `MINOR` findings.
4. Include positive patterns only when directly evidenced.
5. Return `needs_context` if code artifacts are missing.

## Output

Use the standard report sections. Do not fabricate validation or CI status.
