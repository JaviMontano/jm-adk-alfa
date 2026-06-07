# Alerting Strategy

Deterministic JM Labs skill for designing alerting strategies that reduce fatigue while preserving escalation for real incidents. It covers severity classification, actionable alert rules, ownership, routing, escalation, suppression, deduplication, review cadence, and validation.

## Trigger

Use this skill when the request asks for alerting strategy, severity classification, escalation rules, on-call routing, alert fatigue prevention, alert thresholds, deduplication, suppression windows, or incident paging policy.

## Output Contract

The strategy must include system context, evidence, severity model, alert rules, escalation paths, fatigue controls, routing policy, validation checks, and residual risks. JSON handoffs are validated offline with `scripts/validate_alerting_strategy.py`.
