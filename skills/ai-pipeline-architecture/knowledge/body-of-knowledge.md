# AI Pipeline Architecture Body of Knowledge

## Canon

The pipeline is the architecture. The model is one component inside development,
production, registry, CI/CD, monitoring, and requirements systems.

## Required Coverage

| Area | Deterministic Requirement |
|------|---------------------------|
| Development pipeline | at least one allowed development stage with gates |
| Production pipeline | at least one allowed production stage with gates |
| Data stores | allowed store types with latency and consistency rationale |
| Model registry | artifact versioning, lineage, stage management, rollback |
| CI/CD | model, feature, data, performance, security, regression gates |
| Requirements | AP/NF/SEC/CP ids mapped to components |

## Anti-Patterns

- one pipeline for experimentation and production
- direct file copy instead of model registry
- production deploy without regression gate
- store choice by vendor preference instead of workload
- requirements without measurable thresholds or mapped components
