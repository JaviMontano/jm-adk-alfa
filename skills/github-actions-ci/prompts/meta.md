---
name: github-actions-ci-meta
type: self-improvement
version: 2.0.0
description: "Evaluate and improve deterministic GitHub Actions CI/CD planning."
---

# GitHub Actions CI/CD - Self-Improvement

## Evaluate

1. Do new workflow types require new trigger, permission, or deploy policies?
2. Did any real workflow require a safe exception to action pinning or cache
   invalidation?
3. Are invalid fixtures rejecting broad permissions, inline secrets, unpinned
   actions, PR deploys, and missing validation?
4. Do evals still cover false positives, degradation, conflicts, and boundaries?

## Improve

1. Add a fixture before changing validator behavior.
2. Update assets before prompts so policy remains the source of truth.
3. Add evals for new false-positive or false-negative patterns.
4. Record non-automatable GitHub settings, such as repository secrets or
   environment reviewers, as handoff risks.

## Trigger

Run this meta-prompt when a workflow plan fails review, a new deploy target is
introduced, or the validator rejects a legitimate workflow plan.
