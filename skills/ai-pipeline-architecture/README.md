# AI Pipeline Architecture

Designs source-backed AI pipeline architecture packets covering development
pipeline stages, production pipeline stages, data stores, model registry, CI/CD
strategy, and AP/NF/SEC/CP requirements.

## Triggers

- "design AI pipelines"
- "architect ML pipelines"
- "select data stores for AI"
- "design model registry"
- "implement CI/CD for ML"
- "define AI pipeline requirements"

## Deterministic Output

The hardened output is a JSON-compatible architecture packet with:

- system context and evidence ids
- development and production pipeline stages
- data store selection with workload rationale
- model registry versioning, lineage, stage management, and rollback
- Blue-Gold or equivalent CI/CD strategy and validation gates
- AP/NF/SEC/CP requirement mapping
- validation checks and risks

## Offline Validation

Run:

```bash
bash skills/ai-pipeline-architecture/scripts/check.sh
```

The validator uses only local assets and fixtures.
