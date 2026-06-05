# Benchmark Skill Knowledge Graph

## Core Concepts

- benchmark-rubric: 10 quality dimensions
- gate-policy: 13 pass/fail checks
- net-assessment-policy: label rules
- report-contract: required report shape
- deterministic-validator: local JSON report validator
- comparison-framework: scoring consistency and trade-off reference

## Dependencies

- Upstream: State A, State B, skill paths, git refs, or standard mode
- Downstream: benchmark report, regression table, recommendation, caveats

## Relationships

- `benchmark-skill` produces `benchmark-report`
- `benchmark-report` is validated by `report-contract`
- `dimension_scores` are scored by `benchmark-rubric`
- `gate_changes` are scored by `gate-policy`
- `summary.net_assessment` is classified by `net-assessment-policy`
- `comparison-framework` calibrates human scoring evidence
