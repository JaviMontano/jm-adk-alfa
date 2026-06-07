---
name: error-recovery-automation-meta
type: self-improvement
version: 2.0.0
description: "Evaluate and improve the deterministic recovery skill."
---

# Error Recovery Automation - Self-Improvement

## Evaluate

1. Are new failure classes needed in `assets/classification-policy.json`?
2. Did any real recovery require a retry exception, rollback exception, or new
   escalation trigger?
3. Do fixtures cover both accepted and rejected recovery plans?
4. Are eval cases still tied to assets, deterministic scripts, and quality
   criteria?
5. Do examples avoid claiming recovery without validation evidence?

## Improve

1. Add a fixture before weakening the validator.
2. Add eval cases for any new false positive or false negative.
3. Update assets before updating prompts so the policy remains the source of
   truth.
4. Record residual risk in the review doc when a policy cannot be validated
   offline.

## Trigger

Run this meta-prompt when a recovery plan fails review, a new failure mode is
encountered, or the offline validator rejects a legitimate plan.
