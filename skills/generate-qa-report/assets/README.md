# generate-qa-report Assets

These assets define deterministic policy for QA report aggregation.

- `report-contract.json`: required report fields, evidence tags, and moving-time terms.
- `severity-policy.json`: allowed severities and status values.
- `source-policy.json`: QA source dimensions and categories.
- `output-policy.json`: TL;DR, finding, and recommendation limits.

The offline validator reads these assets and fixtures in `scripts/fixtures/`.
