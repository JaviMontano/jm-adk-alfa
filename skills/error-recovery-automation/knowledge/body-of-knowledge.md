# Error Recovery Automation - Body of Knowledge

## Canon

Recovery automation is safe only when the failure class, state impact, retry
bounds, rollback path, escalation owner, and validation evidence are explicit.
Blind reruns are unsafe because they can hide root cause, duplicate side
effects, or corrupt state.

## Error Classes

| Class | Retry Default | Required Handling |
|-------|---------------|-------------------|
| `timeout` | Allowed with bounds | Confirm idempotency, use deterministic backoff, validate after retry |
| `rate_limit` | Allowed with bounds | Respect stop conditions and avoid random jitter |
| `transient_network` | Allowed with bounds | Confirm network symptom and stop on class change |
| `dependency_unavailable` | Allowed with bounds | Confirm dependency evidence and stop on class change |
| `schema_contract` | Blocked | Fix contract mismatch before retry |
| `auth_failed` | Blocked | Escalate to credential or permission owner |
| `configuration_error` | Blocked | Correct configuration and validate before retry |
| `data_integrity` | Blocked | Preserve state and require owner review |
| `unknown` | Blocked | Gather evidence before classification |

## Recovery Invariants

- Retry must be bounded by maximum attempts and maximum delay.
- Retry must be idempotent or protected by a rollback plan.
- Rollback must include verification, not only an action list.
- Escalation must include owner, trigger, handoff evidence, and requested
  decision.
- Recovery is complete only after post-recovery validation passes.

## Quality Metrics

| Metric | Target | How to Measure |
|--------|--------|---------------|
| Classification coverage | 100% | Every plan names an error class and recoverability |
| Retry safety | 100% | Retry plans include bounds, idempotency, and stop conditions |
| Rollback coverage | 100% | Stateful recoveries include rollback and verification |
| Evidence coverage | 100% | Claims, commands, and validation outcomes are traceable |
| Escalation coverage | 100% | Non-retryable plans identify owner and handoff evidence |

## References

- `assets/classification-policy.json`
- `assets/retry-policy.json`
- `assets/rollback-policy.json`
- `assets/escalation-policy.json`
- `assets/evidence-policy.json`
- `scripts/validate_error_recovery.py`
