---
name: ai-assisted-testing-meta
type: self-improvement
version: 2.0.0
description: "Evaluate and improve the AI Assisted Testing skill."
---

# AI Assisted Testing — Self-Improvement

## Evaluate

1. Do policies still cover unit, integration, property, fuzz, mutation, regression, and coverage work?
2. Do fixtures reject unsafe fuzzing and tests without oracles?
3. Do templates preserve proposed vs executed status?
4. Are new testing frameworks or languages represented as optional evidence, not hard dependencies?

## Improve

1. Update assets first.
2. Add fixtures for every new rejection rule.
3. Update eval cases.
4. Re-run `scripts/check.sh` and repo validators.

## Trigger

Run this meta-prompt when:
- A generated plan lacks oracles.
- Fuzzing or mutation guidance changes.
- Coverage optimization produces uncheckable claims.
