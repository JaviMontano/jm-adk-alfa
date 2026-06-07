# Example Output

## System Context

- system: `Claims Assist`
- use_case: healthcare claims triage
- risk_level: high
- strategy_scope: AI testing strategy

## Evidence

| id | tag | source | summary |
|---|---|---|---|
| E1 | [EXPLICIT] | user input | FastAPI, Python ingestion, PostgreSQL, S3, registry, and gradient boosting model are declared. |
| E2 | [EXPLICIT] | user input | p95 inference below 250 ms, weekly retraining, PHI-safe audit, and deterministic fallback are required. |
| E3 | [EXPLICIT] | user input | Known gaps include skew, stale distributions, drift alerts, fairness tests, and model promotion gates. |
| E4 | [EXPLICIT] | user input | Test data must be synthetic or de-identified. |

## Matrix Coverage

| test_type | layer | priority | coverage_target |
|---|---|---|---|
| functional | API | mandatory | API contract and response schema |
| performance | Model Processing | mandatory | p95 inference < 250 ms |
| security | Data Management | mandatory | no raw PHI in fixtures or logs |
| compliance | Pipeline Ops | mandatory | model promotion evidence retained |
| fairness | Model Processing | mandatory | parity >= 90% threshold |
| integration | Pipeline Ops | mandatory | ingestion to scoring path validated |

## Model Tests

- accuracy: holdout and slice metrics with regression gate.
- adversarial: boundary and perturbation tests for claim amount and document quality.
- drift: PSI simulation with alert threshold and retraining review trigger.
- counterfactual: reviewer-priority sensitivity checks.
- regression: challenger must not degrade any protected or high-value slice.

## Data Quality Tests

- schema: claims schema, required fields, formats, ranges.
- distribution: claim amount, provider, procedure code, and document count drift.
- lineage: source-to-prediction lineage queryable by claim id and model version.
- training_serving_skew: feature computation parity between batch training and API scoring.

## Fairness And Compliance Tests

- fairness: demographic parity, equal opportunity, and disparate impact by approved protected groups.
- audit_trail: every prediction logs model version, feature version, confidence, explanation id, and decision path.
- privacy: PHI detection and redaction tests for fixtures, logs, and audit export.
- governance: model promotion requires approval, evaluation report, and rollback plan.

## Integration Strategy

- approach: bottom_up_harness
- rationale: healthcare risk makes data and compliance evidence the first gate.
- contracts: data contract, feature contract, model contract, API contract.

## Automation Gates

| gate | tier | trigger | blocks |
|---|---|---|---|
| code_quality | T1 | every commit | yes |
| data_quality | T2 | every PR | yes |
| model_quality | T3 | pre-deploy | yes |
| fairness_compliance | T5 | model promotion | yes |
| performance_regression | T4 | release candidate | yes |

## Monitoring

- drift: detect input distribution drift within 1 hour.
- performance: alert when p95 exceeds 250 ms.
- fairness: track parity after deployment on approved slices.

## Validation

- assets
- deterministic_scripts
- quality_criteria
- matrix_coverage
- model_test_coverage
- data_quality_coverage
- fairness_compliance_coverage
- automation_gates
