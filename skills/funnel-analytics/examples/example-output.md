# Example Output

## Summary

[CÓDIGO] The provided tracking plan and dashboard define a six-step SaaS signup-to-activation funnel for 2026-05-01 through 2026-05-30 UTC. [CÓDIGO] The largest verified relative drop-off is between `workspace_created` and `invite_sent`: 1,910 to 850 users, a 55.5% drop-off. [CONFIG] Treat bot filtering and any causal explanation as `not verified` until source-owner validation or research evidence is provided.

## Funnel Definition

| Step | Event | Unit | Count | Evidence Status |
|---|---|---|---:|---|
| 1 | `landing_viewed` | user | 12,400 | verified from provided dashboard |
| 2 | `signup_started` | user | 3,100 | verified from provided dashboard |
| 3 | `signup_completed` | user | 2,480 | verified from provided dashboard |
| 4 | `workspace_created` | user | 1,910 | verified from provided dashboard |
| 5 | `invite_sent` | user | 850 | verified from provided dashboard |
| 6 | `first_report_exported` | user | 420 | verified from provided dashboard |

## Drop-Off Analysis

| Step Pair | Entered | Converted | Drop-Off | Interpretation |
|---|---:|---:|---:|---|
| Landing to signup start | 12,400 | 3,100 | 75.0% | [CÓDIGO] Highest absolute loss; channel and intent mix need segmentation. |
| Signup start to completion | 3,100 | 2,480 | 20.0% | [CÓDIGO] Lower relative loss; validate form errors before recommending UI changes. |
| Signup completion to workspace | 2,480 | 1,910 | 23.0% | [CÓDIGO] Activation setup may be a measurement or product gap. |
| Workspace to invite | 1,910 | 850 | 55.5% | [CÓDIGO] Largest verified relative post-signup loss. |
| Invite to export | 850 | 420 | 50.6% | [CÓDIGO] Requires segment and cohort checks before causal claims. |

## Instrumentation Gaps

- [CÓDIGO] Employee and test-account exclusions are provided; bot filtering is `not verified`.
- [CONFIG] Validate that all six events deduplicate by the same user identifier.
- [CONFIG] Add payload checks for `plan_type`, `channel`, and workspace/account identifiers before segment-level action.

## Optimization Backlog

| Hypothesis | Evidence | Metric | Guardrail | Validation |
|---|---|---|---|---|
| Improve post-workspace invite prompt | [CÓDIGO] 55.5% drop-off from workspace to invite | invite rate | workspace completion | A/B test after event dedupe validation |
| Improve export onboarding after invite | [CÓDIGO] 50.6% drop-off from invite to export | first export rate | invite sent rate | Experiment plus user-session review |
| Segment top-of-funnel by channel | [CÓDIGO] 75.0% landing-to-start drop-off | signup start rate | qualified traffic mix | Channel cohort report |

## Validation

- [CÓDIGO] Counts, units, and window come from the user-provided dashboard.
- [CONFIG] Causality is not claimed.
- [CONFIG] Gaps use `not verified` instead of invented values.
- [CONFIG] Privacy is preserved by using aggregate counts only.
