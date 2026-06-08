---
name: generate-qa-scorecard-meta
type: self-improvement
version: 2.0.0
description: "Evaluate and improve deterministic QA scorecard generation."
---

# Generate QA Scorecard - Self-Improvement

## Evaluate

1. Are dimension names and order still aligned with `assets/dimensions-policy.json`?
2. Did any real scorecard reveal a missing severity, grade, or action rule?
3. Are invalid fixtures rejecting status mismatch, grade mismatch, missing
   dimensions, and bad action ranking?
4. Do eval cases still cover happy paths, reduced scope, false positives, and
   no-evidence degradation?

## Improve

1. Add a fixture before changing score or ranking behavior.
2. Update assets before prompts so policy remains the source of truth.
3. Add eval cases for every new false-positive or false-negative pattern.
4. Record scoring caveats in the review doc when a scenario cannot be validated
   offline.

## Trigger

Run this meta-prompt when a scorecard fails review, a dimension changes, or the
offline validator rejects a legitimate scorecard.
