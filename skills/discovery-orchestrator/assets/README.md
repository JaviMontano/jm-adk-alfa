# Discovery Orchestrator Assets

These assets convert discovery orchestration into deterministic contracts. They are meant to be reused by prompts, examples, evals, and offline scripts without requiring network, current time, or random choices.

## Inventory

- `phase-contract.json`: allowed phase ids, order, status values, and required phase fields.
- `skill-sequence-contract.json`: canonical downstream discovery skills and required sequence fields.
- `gate-policy.json`: G1, feasibility checkpoint, G2, and G3 pass/block criteria.
- `non-analysis-boundary.json`: forbidden analysis, implementation, and price leakage fields.
- `report-contract.json`: top-level orchestration packet fields, modes, and evidence tags.

## Deterministic Use

Use explicit `reference_date` values. Do not use moving terms such as `today`, `tomorrow`, `soon`, or `TBD`. A gate may be `pass`, `block`, or `pending`; only explicit evidence and approval can produce `pass`.
