# Benchmark Skill Assets

Deterministic assets for benchmark reports.

- `benchmark-rubric.json`: 10 scoring dimensions, bounds, and evidence rules.
- `gate-policy.json`: 13 quality gates used in version and standard comparisons.
- `net-assessment-policy.json`: exact classification rules.
- `report-contract.json`: required report sections, labels, and blocked vague
  phrases.

Use these assets before producing the report. When a JSON report is available,
validate it with `scripts/validate_benchmark_report.py`.
