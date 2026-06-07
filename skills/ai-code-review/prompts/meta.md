---
name: ai-code-review-meta
type: self-improvement
version: 2.1.0
description: "Evaluate and improve the deterministic AI Code Review skill."
---

# AI Code Review - Self-Improvement

## Evaluate
1. Do evals still include false positives, fake test claims, clean reviews, and low-confidence degradation?
2. Do assets still match the validator contract?
3. Do examples include exact file-line evidence and scope exclusions?
4. Do prompts prevent speculative P0/P1 findings?
5. Are new review categories needed for recurring repository patterns?

## Improve
1. Add new fixtures for any false positive that escaped the policy.
2. Update `assets/severity-policy.json` only when priority semantics change.
3. Keep `scripts/check.sh` offline and deterministic.
4. Update review doc and ledger only after validation evidence exists.

## Trigger
Run this meta-prompt after failed review validation, user-reported false positives,
or new recurring review categories.
