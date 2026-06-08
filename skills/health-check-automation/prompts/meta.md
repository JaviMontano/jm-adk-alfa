---
name: health-check-automation-meta
type: self-improvement
version: 2.0.0
description: "Evaluate and improve deterministic health-check automation."
---

# Health Check Automation - Self-Improvement

## Evaluate

1. Do new health surfaces require new check types or thresholds?
2. Did any real report need a status not covered by pass, warn, fail, or
   unknown?
3. Are invalid fixtures rejecting false healthy decisions?
4. Are alert owner and handoff requirements still complete?
5. Do evals still include false positives, stale evidence, degradation, and
   missing owner cases?

## Improve

1. Add a fixture before changing validator behavior.
2. Update assets before prompts so policy remains the source of truth.
3. Add evals for every new false-positive or false-negative pattern.
4. Record non-automatable evidence gaps in the review doc.

## Trigger

Run this meta-prompt when a health report fails review, a new monitor type is
introduced, or the validator rejects a legitimate report.
