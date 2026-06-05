# Code Review - Body of Knowledge

## Canon

Deterministic code review evaluates supplied evidence against a fixed taxonomy.
The review must distinguish inspected code facts from risk inference, keep
style feedback non-blocking unless policy requires it, and never invent files,
tests, CI status, or runtime behavior.

## Review Dimensions

| Dimension | Primary question | Blocking signal |
|---|---|---|
| Correctness | Does the code satisfy the stated behavior? | likely crash, wrong result, broken edge case, data loss |
| Security | Does the diff weaken trust boundaries? | auth bypass, injection, secret exposure, privilege issue |
| Tests | Do tests cover new behavior and failure paths? | missing required regression or failing supplied CI |
| Performance | Can the change regress critical paths? | unbounded query/loop, avoidable N+1 on core path |
| Maintainability | Can future maintainers understand and change it? | confusing abstraction on risky code path |
| API contract | Does it preserve documented interfaces? | breaking response shape, signature, status code, schema |
| Observability | Can failures be diagnosed? | removed critical logging/metrics on risky path |
| Style | Does it violate enforced conventions? | only blocking when backed by explicit policy |

## Severity Calibration

- `BLOCKER`: should block merge because a cited defect can break correctness,
  security, data integrity, or required validation.
- `MAJOR`: material issue, not an immediate release blocker without added
  context.
- `MINOR`: improvement with limited risk.
- `NIT`: style/readability preference; never a blocker without policy evidence.

## Evidence Rules

- Code findings require file and line.
- Missing context is reported as `needs_context`, not as a finding.
- Inference must be linked to a cited code fact.
- Positive patterns are required for clean approvals.
- Secret-like values are redacted in output.

## Decision Rules

- Any `BLOCKER` => `request_changes`.
- Findings without `BLOCKER` => `approve_with_comments`.
- No findings plus positive patterns => `approve`.
- Missing minimum inputs => `needs_context`.
