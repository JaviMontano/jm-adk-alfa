# Generate QA Report - Knowledge Graph

## Core Concepts
- generate-qa-report: QA evidence aggregator
- source-run: validation or audit source with status and evidence
- finding: normalized issue record
- summary-stats: reconciled severity totals
- category-status: PASS, WARN, FAIL, or NOT_RUN per category
- recommendation: ranked action linked to findings
- report-contract: deterministic output schema

## Dependencies
- Upstream: validation and audit skills
- Downstream: changelog, release readiness, remediation planning

## Skill Relationships
Part of the JM Labs canonical skill registry. It should run after validation sources exist.
