# Error Recovery Automation Assets

These assets define the deterministic contract for recovery plans.

## Files

- `error-recovery-contract.json`: required output sections and structured JSON
  fields.
- `classification-policy.json`: error classes, recoverability defaults, and
  retry eligibility.
- `retry-policy.json`: bounded retry, deterministic backoff, idempotency, and
  stop conditions.
- `rollback-policy.json`: rollback requirements for stateful or destructive
  recovery.
- `escalation-policy.json`: owner handoff requirements for non-retryable or
  uncertain failures.
- `evidence-policy.json`: evidence required before classification, retry, and
  closure.

Use these assets before changing prompts or examples so policy remains the
source of truth.
