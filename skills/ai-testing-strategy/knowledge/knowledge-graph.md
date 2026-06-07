# AI Testing Strategy - Knowledge Graph

## Core Nodes

- `ai-testing-strategy`: skill capability.
- `system-context`: system, use case, risk level, scope.
- `evidence`: explicit, inferred, or open provenance.
- `matrix-coverage`: six test types and six layers.
- `model-tests`: accuracy, adversarial, drift, counterfactual, regression.
- `data-quality-tests`: schema, distribution, lineage, training-serving skew.
- `fairness-compliance-tests`: fairness, audit trail, privacy, governance.
- `integration-strategy`: approach, harness, contracts.
- `automation-gates`: CI/CD test gates and blocking policy.
- `monitoring`: drift, performance, fairness, and model quality monitoring.
- `validation`: deterministic completion checks.

## Relationships

- `ai-testing-strategy` requires `system-context`.
- `system-context` is supported by `evidence`.
- `matrix-coverage` contains `model-tests`, `data-quality-tests`, and `fairness-compliance-tests`.
- `integration-strategy` validates cross-component flow.
- `automation-gates` enforce test execution.
- `monitoring` extends testing after deployment.
- `validation` checks all prior nodes.
