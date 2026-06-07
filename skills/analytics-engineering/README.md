# Analytics Engineering

Use this skill to design deterministic analytics transformation layers, dbt-style model contracts, tests, lineage, and documentation for a data warehouse or lakehouse program.

## Trigger Signals

- Source-to-target mapping across raw, staging, intermediate, mart, and metrics layers.
- dbt, SQLMesh, Dataform, stored procedure migration, or transformation framework architecture.
- Star schema, one-big-table, activity schema, slowly changing dimensions, or bridge tables.
- Materialization decisions for views, tables, incremental models, snapshots, or ephemeral models.
- Data contracts, mart tests, lineage, exposures, freshness, and documentation plans.

## Deterministic Deliverable

The output must identify the project scope, evidence, sources, models, tests, contracts, lineage, documentation, validation checks, assumptions, and risks. Every production mart needs an explicit grain, owner, materialization, upstream lineage, and blocking tests.

## Assets

The `assets/` directory defines the offline contract:

- `analytics-engineering-contract.json` lists required sections and validation checks.
- `layer-policy.json` defines layer names, prefixes, and valid materializations.
- `materialization-policy.json` defines fields needed for incremental and non-incremental models.
- `testing-policy.json` defines accepted test types and required mart coverage.
- `data-contract-policy.json` defines contract enforcement and breaking-change policy.
- `evidence-policy.json` defines evidence tags and required provenance fields.

## Scripts

Run `bash skills/analytics-engineering/scripts/check.sh` to validate deterministic JSON fixtures. The script accepts valid analytics engineering handoffs and rejects missing evidence, unsupported materializations, weak mart tests, broken lineage, unenforced contracts, and incomplete validation checks.

## Output Shape

The default user-facing format is Markdown. When a machine-checkable handoff is needed, emit JSON matching `assets/analytics-engineering-contract.json` and validate it with `scripts/validate_analytics_engineering.py`.
