# Example Output — AI Architecture Audit

## Executive Summary

`claims-risk-ai` has high operational and governance risk: direct production deployment, missing drift monitoring, no automated fairness testing, and latency above threshold. [CÓDIGO]

## Six-Dimension Scorecard

| Dimension | Score | Status |
|-----------|-------|--------|
| D1 Structural Integrity | 3 | Partial layer separation documented |
| D2 AI Quality Attributes | 2 | Drift and fairness controls missing |
| D3 Pattern Adherence | 2 | Missing champion-challenger and circuit breaker |
| D4 Security & Compliance | 3 | Endpoint controls need evidence |
| D5 Technical Debt | 2 | Drift, test, and deployment debt present |
| D6 Remediation Roadmap | 4 | Prioritized fixes available |

## Top Findings

| id | severity | dimension | finding | evidence |
|----|----------|-----------|---------|----------|
| F-001 | HIGH | D2 | Drift detection is absent for production scoring. | Monitoring export has no drift alert policy. [MÉTRICA] |
| F-002 | HIGH | D3 | Deployment path matches YOLO Deploy anti-pattern. | `infra/model-serving.yaml` deploys main directly to production. [CONFIG] |
| F-003 | MEDIUM | D2 | Fairness testing is manual and not repeatable. | Team interview says fairness testing is not automated. [ENTREVISTA] |

## Remediation Roadmap

1. Add drift monitoring and alert policy with retraining triggers. Pattern: Drift Detection. Effort: M. DoD: drift dashboard and alert test pass. [INFERENCIA]
2. Add staging/canary gate before production deploy. Pattern: Blue & Gold CI/CD. Effort: L. DoD: canary deploy and rollback documented. [INFERENCIA]
3. Add automated fairness tests to CI. Pattern: Responsible AI test suite. Effort: M. DoD: fairness threshold gate blocks regressions. [INFERENCIA]

## Validation

- Six dimensions covered. [CÓDIGO]
- Findings include evidence and severity. [CÓDIGO]
- Remediations include pattern, effort, dependencies, and DoD. [CÓDIGO]
