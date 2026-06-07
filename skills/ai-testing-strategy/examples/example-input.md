# Example Input

Define the AI testing strategy for `Claims Assist`, a healthcare claims triage system.

Context:
- Stack: FastAPI scoring API, Python batch ingestion, PostgreSQL, S3 document archive, model registry, and batch-trained gradient boosting model.
- Required outcomes: p95 inference below 250 ms, weekly retraining, PHI-safe audit trail, no raw PHI in model logs, and deterministic fallback rules.
- Known risks: training-serving skew, stale feature distributions, missing drift alerts, incomplete fairness testing, and no automated model promotion gate.
- Test data constraints: production PHI cannot be copied into test fixtures; synthetic or de-identified datasets are required.

Produce a deterministic testing strategy with matrix coverage, model tests, data quality tests, fairness and compliance tests, integration approach, CI/CD gates, monitoring checks, residual risks, and validation evidence.
