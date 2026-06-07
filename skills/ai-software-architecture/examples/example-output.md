# Example Output

## System Context

- system: `Claims Assist`
- use_case: healthcare claims triage
- risk_level: high
- architecture_scope: logical AI software architecture

## Evidence

| id | tag | source | summary |
|---|---|---|---|
| E1 | [EXPLICIT] | user input | Python workers, PostgreSQL, S3, FastAPI, and batch-trained model are declared components. |
| E2 | [EXPLICIT] | user input | p95 inference target is below 250 ms and weekly retraining is required. |
| E3 | [INFERRED] | architecture analysis | PHI logging constraints require audit-safe observability and redacted model telemetry. |

## 6-Layer Module View

| layer | modules | responsibility | dependencies | owner |
|---|---|---|---|---|
| hardware | CPU inference pool | serve triage model without GPU dependency | container platform | platform |
| data | claims ingestion, feature builder, feature store | validate schemas and compute reusable features | PostgreSQL, S3 | data engineering |
| model | triage model, model registry | version model artifacts and evaluation metadata | feature store | ML engineering |
| inference | FastAPI scoring adapter, fallback rules | return priority and confidence under SLA | model registry, feature store | application engineering |
| application | case API, review queue | expose triage outcome to claims workflow | inference adapter | product engineering |
| monitoring_control | drift monitor, audit logger, alert rules | track model, data, and compliance health | all layers | platform and compliance |

## Selected Patterns

- Feature Store: selected to reduce training-serving skew and centralize feature definitions.
- Drift Detection: selected because weekly retraining does not catch sudden claims mix changes.
- Explainability Wrapper: selected to support audit trails and reviewer trust.
- Circuit Breaker: selected to route requests to fallback rules when model serving fails.

## Quality Attribute Scenarios

| attribute | stimulus | response | measure |
|---|---|---|---|
| performance | 100 concurrent scoring requests | scoring adapter returns priority | p95 < 250 ms |
| availability | model endpoint unavailable | fallback rules serve deterministic priority | failover < 30 s |
| drift_resilience | PSI exceeds threshold on claim amount features | drift alert opens retraining review | detection < 1 h |
| explainability | reviewer opens a triage decision | top drivers and model version are shown | audit trail completeness = 100% |
| compliance | PHI-bearing claim field reaches logs | redaction gate blocks raw value | no raw PHI in model logs |

## ADRs

| id | title | status | decision | consequences |
|---|---|---|---|---|
| ADR-001 | Adopt feature store for claims features | proposed | Shared feature definitions are versioned and served to training and inference. | Reduces skew; adds platform ownership and migration work. |
| ADR-002 | Use rule fallback for model outage | accepted | Deterministic rules serve priority when model endpoint fails. | Preserves availability; may reduce accuracy during outage. |

## Debt And Evolution

- D1 training-serving skew: high severity, mitigated by feature store migration.
- D2 missing drift alerts: high severity, mitigated by PSI and performance monitors.
- D3 unclear ownership: medium severity, mitigated by module-to-team ownership map.

## Validation

- assets
- deterministic_scripts
- quality_criteria
- layer_coverage
- pattern_traceability
- adr_completeness
- debt_evolution
