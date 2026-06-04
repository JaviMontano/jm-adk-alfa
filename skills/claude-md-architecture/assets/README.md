# Assets

Deterministic resources for `claude-md-architecture`.

- `architecture-schema.json` defines the required input contract.
- `architecture-policy.json` defines allowed scopes, root limits, import rules, and blocked anti-patterns.
- `architecture-report-template.md` provides the generated report shape.

These assets are consumed by `scripts/compile-claude-md-architecture.py` and verified by `scripts/check.sh`.
