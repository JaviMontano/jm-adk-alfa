# Analytics Engineering Assets

These assets define the deterministic contract for analytics engineering outputs. They are read-only policy files used by prompts, agents, templates, evals, and the local validator.

## Files

- `manifest.json`: DoD asset manifest for this skill.
- `analytics-engineering-contract.json`: Required sections and validation checks.
- `layer-policy.json`: Allowed layer names, model prefixes, and materializations.
- `materialization-policy.json`: Required fields for incremental and full-refresh strategies.
- `testing-policy.json`: Allowed test types and mandatory mart test coverage.
- `data-contract-policy.json`: Contract enforcement and breaking-change rules.
- `evidence-policy.json`: Evidence tags and required provenance fields.

## Determinism

The assets contain static JSON only. They do not call network services, read the clock, or use random sampling.
