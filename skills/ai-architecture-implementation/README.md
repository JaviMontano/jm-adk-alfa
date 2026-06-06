# AI Architecture Implementation

Turn an approved AI architecture, audit roadmap, or implementation request into a phased production plan. The skill covers technology selection, data pipelines, model lifecycle, serving, CI/CD, monitoring, rollback, and runbooks.

Use this skill for AI implementation plans, MLOps setup, feature store rollout, model serving, drift monitoring, RAG implementation, migration from notebooks to production, or remediation execution after an AI architecture audit.

## Deterministic Contract

- Implementation work must be phased; no big-bang plan may pass.
- Each phase must include scope, deliverables, dependencies, evidence, and Definition of Done.
- Technology choices must include selected option, alternatives, rationale, and ADR requirement when non-obvious.
- CI/CD, monitoring, rollback, and runbooks are required for production-oriented plans.
- Missing architecture, data, team, budget, or environment inputs must become risks or prerequisites, not invented assumptions.
- Machine-readable implementation packets must validate with `scripts/check.sh`.
