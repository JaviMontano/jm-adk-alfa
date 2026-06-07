# Error Recovery Automation - Knowledge Graph

## Core Concepts

- [[failure-evidence]] anchors every recovery decision in observed facts.
- [[error-classification]] maps observed errors to retryable, non-retryable, or
  human-required outcomes.
- [[bounded-retry]] permits retry only when attempts, delay, idempotency, and
  stop conditions are explicit.
- [[rollback-plan]] protects state before rerunning commands that may create
  side effects.
- [[escalation-handoff]] transfers non-retryable or uncertain failures to an
  accountable owner.
- [[validation-evidence]] proves recovery before closure.

## Flow

- [[failure-evidence]] -> [[error-classification]]
- [[error-classification]] -> [[bounded-retry]]
- [[error-classification]] -> [[rollback-plan]]
- [[error-classification]] -> [[escalation-handoff]]
- [[bounded-retry]] -> [[validation-evidence]]
- [[rollback-plan]] -> [[validation-evidence]]
