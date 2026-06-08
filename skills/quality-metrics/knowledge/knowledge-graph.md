# Quality Metrics Knowledge Graph

## Core Nodes

- `quality-metrics`: produces a metric scorecard.
- `coverage`: line, branch, function, and statement coverage.
- `complexity`: max cyclomatic complexity.
- `duplication`: duplicated code percentage.
- `lighthouse`: web quality scores.
- `bundle-size`: initial gzipped bundle budget.
- `firestore-io`: daily reads, writes, deletes, and spike multiplier.
- `guardian`: validates score, gates, evidence, and actions.

## Edges

- `quality-metrics` requires `evidence-summary`.
- Each metric requires a gate.
- Metric statuses drive `quality_score`.
- Non-pass metrics drive `priority_actions`.
- `guardian` blocks missing evidence or missing canonical metrics.
