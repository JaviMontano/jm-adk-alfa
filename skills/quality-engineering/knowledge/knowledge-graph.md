# Quality Engineering Knowledge Graph

## Core Nodes

- `quality-engineering`: produces a quality framework.
- `maturity-assessment`: scores six dimensions.
- `test-strategy`: maps architecture to test distribution.
- `quality-gates`: defines commit, PR, nightly, release, and production gates.
- `metrics-dashboard`: combines leading and lagging indicators.
- `priority-actions`: ranks the largest maturity gaps.
- `guardian`: decides pass, warn, or block.

## Edges

- `quality-engineering` requires `evidence-summary`.
- `maturity-assessment` drives `priority-actions`.
- `architecture-type` selects `test-strategy`.
- `quality-gates` enforce `metrics-dashboard` and release readiness.
- `guardian` validates all contracts before handoff.
