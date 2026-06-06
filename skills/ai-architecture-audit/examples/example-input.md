# Example Input — AI Architecture Audit

Audit the architecture of `claims-risk-ai`, an ML scoring service used in claims triage.

Available evidence:

- Repository contains `pipelines/features.py`, `serving/app.py`, and `infra/model-serving.yaml`.
- Deployment config shows direct deploy from main to production.
- Monitoring export includes latency P95 `820ms`, availability `99.7%`, and no drift alert policy.
- Architecture document lists data, model, serving, application, and monitoring layers.
- Team interview says fairness testing is not automated.

Scope: full six-dimension audit. Format: hybrid. Do not implement fixes; produce findings and a prioritized remediation roadmap.
