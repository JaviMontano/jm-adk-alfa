# Example Output

## Evidence Summary

- Subject: Project Atlas.
- Architecture: microservices.
- Evidence: eight services, GitHub Actions CI, two Pact contracts, Jest unit tests, partial Playwright coverage, masked lower environments.
- Assumptions: no release gate and no shared dashboard are treated as current gaps.

## Maturity Assessment

| Dimension | Score | Level | Evidence |
|---|---:|---:|---|
| test_strategy | 55 | 3 | Tests exist but strategy is not documented across services. |
| test_automation | 62 | 4 | Jest and Playwright are present; contract coverage is partial. |
| quality_gates_cicd | 48 | 3 | PR checks exist but exceed the target timeout and release gate is absent. |
| test_data_management | 65 | 4 | Regulated customer data is masked in lower environments. |
| quality_metrics_dashboards | 30 | 2 | No shared quality dashboard exists. |
| shift_left_practices | 52 | 3 | Developers own unit tests but gate criteria are not uniform. |

Overall score: 52.0. Overall level: 3. Target level: 4.

## Test Strategy

Shape: `test_diamond`.

| Type | Share |
|---|---:|
| unit | 20 |
| integration | 40 |
| contract | 30 |
| e2e | 10 |

## Quality Gates

- commit: blocking, 5 minutes, unit tests + lint + no critical SAST.
- pr: blocking, 15 minutes, integration + contract + coverage floor.
- nightly: async, 60 minutes, E2E + API regression + performance baseline.
- release: blocking, 120 minutes, load SLA + smoke + security sign-off.
- production: blocking, 15 minutes, smoke + canary metric validation.

## Metrics Dashboard

Leading metrics: review catch rate, coverage, build stability, flaky rate, PR gate time, deployment frequency.

Lagging metrics: production incidents, escaped defects, critical MTTR, regression rate.

## Top Priority Actions

1. Build a shared quality metrics dashboard.
2. Add a blocking release gate with security sign-off.
3. Reduce PR gate time from 18 minutes to 15 minutes or less.

## Guardian Decision

Decision: `warn`.

Reason: The plan is valid, but release gate and quality dashboard evidence are missing.
