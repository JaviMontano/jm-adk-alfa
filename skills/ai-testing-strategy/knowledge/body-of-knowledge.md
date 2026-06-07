# AI Testing Strategy - Body of Knowledge

## Canon

AI testing strategy verifies AI-enabled systems across test types, architecture layers, model behavior, data quality, fairness, compliance, integration, automation, and monitoring. The canonical matrix is the 6 test types x 6 layers reference in `references/testing-matrix.md`.

## Deterministic Quality Metrics

| Metric | Target | How To Measure |
|--------|--------|----------------|
| Matrix coverage | 100% summary coverage | Report names all six test types and all six layers |
| Model test coverage | 5 required categories | Accuracy, adversarial, drift, counterfactual, regression |
| Data quality coverage | 4 required categories | Schema, distribution, lineage, training-serving skew |
| Fairness/compliance coverage | 4 required categories | Fairness, audit trail, privacy, governance |
| Gate traceability | 100% | Every CI/CD gate has tier, trigger, block policy, and evidence |
| Offline validation | pass | JSON handoff passes `scripts/validate_ai_testing_strategy.py` |

## Core Principles

- Data quality testing is the first line of defense for AI systems.
- Model accuracy without fairness, drift, and regression gates is incomplete.
- CI/CD gates must be explicit about whether they block or warn.
- Production monitoring extends the test strategy beyond deployment.
- Privacy constraints shape the test data strategy.

## References

- `references/testing-matrix.md`
- `references/ai-test-types.md`
- `references/integration-approaches.md`
