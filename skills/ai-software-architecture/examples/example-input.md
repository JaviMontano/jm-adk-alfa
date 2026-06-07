# Example Input

Design the AI software architecture for `Claims Assist`, a healthcare claims triage system.

Context:
- Current stack: Python ingestion workers, PostgreSQL claims store, S3 document archive, FastAPI case API, and a batch-trained gradient boosting model.
- Target workflow: classify incoming claims as low, medium, or high manual-review priority.
- Constraints: p95 inference below 250 ms, audit trail for every prediction, no direct PHI in model logs, fallback rules when the model is unavailable, and weekly retraining.
- Known risks: training-serving skew, stale feature definitions, no drift alerts, and unclear ownership between data engineering and application engineering.

Produce a deterministic architecture report with the 6-layer module view, component contracts, pattern selection, quality attribute scenarios, ADRs, debt register, evolution plan, and validation checks.
