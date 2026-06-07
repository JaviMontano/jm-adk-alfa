# AI Code Review Assets

These assets define the deterministic contract for AI-assisted code review.

## Files
- `review-report-contract.json`: required JSON shape for machine-checkable review reports.
- `severity-policy.json`: P0-P3 priority rules and confidence thresholds.
- `evidence-policy.json`: allowed evidence tags and required evidence fields.
- `scope-policy.json`: include/exclude rules for source, generated, vendored, and lock files.
- `false-positive-policy.json`: suppression and degradation rules for uncertain findings.

The offline validator in `scripts/validate_ai_code_review_report.py` enforces
the same contract against deterministic fixtures.
