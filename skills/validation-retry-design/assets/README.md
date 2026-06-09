# Validation Retry Design Assets

These assets define deterministic validation retry loop contracts and offline checks.

## Inventory

- `manifest.json`: deterministic asset inventory.
- `retry-loop-contract.json`: required JSON plan shape.
- `error-feedback-policy.json`: exact error feedback fields.
- `recoverability-policy.json`: recoverable vs not-recoverable classification.
- `retry-budget-policy.json`: retry budget limits.
- `systematic-error-policy.json`: repeated-error stop rule.
- `escalation-policy.json`: escalation packet fields.
- `anti-pattern-policy.json`: blocked blind retry and silent failure patterns.
