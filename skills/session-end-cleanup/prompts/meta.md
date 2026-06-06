---
name: session-end-cleanup-meta
type: self-improvement
version: 2.1.0
description: "Evaluate and improve deterministic closeout behavior for Session End Cleanup."
---

# Session End Cleanup - Self-Improvement

## Evaluate

1. Do recent closeouts preserve failed/skipped checks instead of hiding them?
2. Are tasklog and changelog updates limited to authorized targets?
3. Do examples cover PR-ready, merged, blocked, no-change, and conflict states?
4. Does `scripts/check.sh` reject missing validation evidence and untagged task
   completion?
5. Are evidence tags aligned with the active runtime contract?

## Improve

1. Update `assets/output-contract.json` when a new required section becomes
   stable.
2. Add deterministic fixtures before loosening prose guidance.
3. Add evals for any recurring false-positive activation.
4. Keep the validator offline and free of wall-clock, network, or random inputs.

## Trigger

Run this meta-prompt when closeouts are too vague, mark completion too early, or
fail to help the next session resume quickly.
