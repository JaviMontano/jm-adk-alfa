---
name: code-review-checklist-meta
type: self-improvement
version: 2.1.0
description: "Evaluate and improve deterministic Code Review Checklist."
---

# Code Review Checklist - Self-Improvement

## Evaluate

1. Do evals cover security, Firebase, performance, TypeScript, false positives,
   missing context, and invalid-report contracts?
2. Do assets still match `SKILL.md`, templates, and validator logic?
3. Does the validator reject approval with blocking failures?
4. Are hotfix checklist outputs recording follow-up within 48 hours?
5. Are remote assets, implicit dates, and mutation tools still absent?

## Improve

1. Update assets first.
2. Update fixtures before validator changes.
3. Preserve checklist IDs unless all evals and fixtures are migrated.
4. Run `bash skills/code-review-checklist/scripts/check.sh`.
5. Run per-skill DoD before ledger changes.
