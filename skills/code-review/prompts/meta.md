---
name: code-review-meta
type: self-improvement
version: 2.1.0
description: "Evaluate and improve deterministic Code Review."
---

# Code Review - Self-Improvement

## Evaluate

1. Are activation rules still precise for code review and not generic review?
2. Do evals include clean-code, style-only, security, correctness, tests,
   missing-input, and conflicting-instruction cases?
3. Does `scripts/validate_code_review_report.py` reject false approvals and
   untagged findings?
4. Do templates avoid remote assets, implicit current dates, and fabricated
   context?
5. Does the ledger review doc include command evidence before `dod-complete`?

## Improve

1. Update assets first, then SKILL/prompts/templates to match.
2. Add or adjust fixtures before changing validator logic.
3. Keep severity and category values stable unless all fixtures and evals are
   updated.
4. Re-run `bash skills/code-review/scripts/check.sh`.
5. Re-run per-skill DoD before changing the ledger.

## Trigger

Run this meta-prompt when the skill receives new false positives, misses known
review defects, or the report contract changes.
