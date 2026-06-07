# Analytics Engineering Body of Knowledge

## Canon

Analytics engineering converts raw source data into trusted analytical models. The stable unit of work is a model contract: model name, layer, grain, owner, materialization, upstream dependencies, tests, documentation, and downstream exposure.

## Layer Rules

| Layer | Prefix | Purpose | Default Materialization |
|---|---|---|---|
| staging | `stg_` | Rename, cast, deduplicate, and expose one source table per model | view |
| intermediate | `int_` | Join, pivot, sessionize, or normalize business logic | ephemeral or view |
| mart | `fct_`, `dim_`, `mrt_` | Serve certified consumption models | table or incremental |
| metrics | `met_` | Publish governed metric calculations | table or semantic layer |

## Deterministic Quality Criteria

- Every source has a freshness expectation and evidence reference.
- Every model has an explicit grain and owner.
- Every non-staging model has upstream lineage.
- Every mart has blocking tests for required keys, relationships, accepted values, or business reconciliation.
- Every production mart has an enforced contract or a documented blocking exception.
- Every incremental model defines `unique_key`, `updated_at`, and `incremental_strategy`.
- Every mart column used by downstream consumers has documentation.

## Anti-Patterns

- Naming marts without grain, owner, or tests.
- Using raw tables outside staging models.
- Choosing incremental materialization without a unique key or late-arrival policy.
- Treating documentation as separate from the model.
- Claiming lineage or source freshness without evidence.
