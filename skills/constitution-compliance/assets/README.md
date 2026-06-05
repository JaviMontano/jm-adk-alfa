# Constitution Compliance Assets

Deterministic assets for Constitution v6.0.0 compliance reports.

- `constitution-v6-principles.json`: 18-principle map, v5.2.0 crosswalk, and
  G0-G3 gates.
- `compliance-report-contract.json`: report sections, status values, evidence
  tags, and blocked phrases.
- `severity-policy.json`: P0-P3 severity and delivery decision rules.
- `activation-policy.json`: activation, false-positive, missing-evidence, and
  version-drift rules.

Use these assets before delivering any compliance report, then validate JSON
fixtures with `scripts/validate_constitution_report.py`.
