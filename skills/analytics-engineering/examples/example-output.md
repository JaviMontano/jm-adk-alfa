# Example Output

## Summary

`Atlas Commerce` should use dbt layers `staging`, `intermediate`, and `marts`, with finance-owned revenue marts and product-owned session marts. Evidence comes from the named Stripe, Salesforce, and app event sources supplied in the request.

## Source-to-Target Mapping

| Source | Staging Model | Downstream Models | Freshness |
|---|---|---|---|
| `stripe.payments` | `stg_stripe_payments` | `int_revenue_events`, `fct_revenue` | 1 hour |
| `stripe.subscriptions` | `stg_stripe_subscriptions` | `int_revenue_events`, `dim_subscription` | 1 hour |
| `salesforce.accounts` | `stg_salesforce_accounts` | `dim_account` | 4 hours |
| `app.events` | `stg_app_events` | `int_sessions`, `fct_sessions` | 1 hour |

## Model Plan

| Model | Layer | Grain | Materialization | Owner |
|---|---|---|---|---|
| `stg_stripe_payments` | staging | one row per payment id | view | Finance Analytics |
| `int_revenue_events` | intermediate | one row per normalized revenue event | ephemeral | Finance Analytics |
| `fct_revenue` | mart | one row per revenue event | incremental merge | Finance Analytics |
| `stg_app_events` | staging | one row per event id | view | Product Analytics |
| `int_sessions` | intermediate | one row per session id | incremental merge | Product Analytics |
| `fct_sessions` | mart | one row per session id | incremental merge | Product Analytics |

## Tests And Contracts

- `fct_revenue`: `not_null` on `revenue_event_id`, `unique` on `revenue_event_id`, `relationships` to `dim_account`, and custom reconciliation against Stripe daily totals.
- `fct_sessions`: `not_null` and `unique` on `session_id`, accepted values for event platform, and late-arrival window reconciliation.
- Production marts enforce contracts with breaking changes blocked in CI.
- Slim CI runs `dbt build --select state:modified+ --defer --state prod-artifacts/`.

## Validation

- Contract sections: sources, models, tests, data contracts, lineage, documentation, validation.
- Deterministic oracle: `bash skills/analytics-engineering/scripts/check.sh`.
- Blocking risks: missing source freshness, unowned marts, unenforced contracts, or lineage gaps.
