# AI Design Patterns - Body of Knowledge

## Canon
AI design patterns are architectural decisions justified by system requirements,
quality attributes, risks, anti-patterns, and operational constraints.

## Pattern Selection Rules
- Recommend only catalogued patterns.
- Pair each pattern with rationale, trade-offs, tactics, dependencies, and evidence.
- Map anti-patterns to remediation patterns.
- Avoid heavy infrastructure patterns when the context does not need them.
- Roadmaps require exit criteria.

## Core Catalog
- Feature Store
- Model Registry
- Champion-Challenger
- Shadow Deployment
- Drift Detection
- Explainability Wrapper
- Canary Deployment
- Bulkhead
- Circuit Breaker
- Guardrail Pattern
- N-Party Voting
- Prompt Caching
- Model Distillation

## Anti-Pattern Mapping
| Anti-Pattern | Typical Fix |
|--------------|-------------|
| Training-Serving Skew | Feature Store |
| YOLO Deploy | Shadow Deployment, Canary Deployment |
| Silent Model Degradation | Drift Detection |
| Feature Sprawl | Feature Store |
| Compliance Afterthought | Explainability Wrapper |
| Monolithic Pipeline | Bulkhead |

## Validation Boundary
`scripts/validate_ai_design_patterns_report.py` validates the report packet,
not the actual implementation of the architecture.
