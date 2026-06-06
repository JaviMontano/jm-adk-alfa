# ideate-component Assets

These assets define the deterministic contract for component concept cards.

- `concept-card-contract.json`: required top-level fields, evidence tags, candidate count, source modes, known tools, and output decisions.
- `component-type-policy.json`: allowed component types, hook compatibility, and type-specific relationship requirements.
- `moat-depth-policy.json`: MOAT depth thresholds, required assets, and line ranges by component type.
- `conflict-policy.json`: conflict statuses and allowed resolutions.

The offline validator reads these files and validates fixtures in `scripts/fixtures/`.
