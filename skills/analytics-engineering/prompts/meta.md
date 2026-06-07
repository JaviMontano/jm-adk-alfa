---
name: analytics-engineering-meta
type: meta
version: 2.0.0
description: "Meta-prompt for Analytics Engineering skill routing."
---

# Analytics Engineering — Meta Prompt

Activate this skill when the user request matches:
- Trigger phrases from SKILL.md description
- Direct invocation: `/analytics-engineering`
- Requests for source-to-target mapping, dbt/SQLMesh/Dataform models, model layers, materialization strategy, data contracts, mart tests, lineage, or documentation plans

## Skill Routing
1. Load SKILL.md and confirm the request is about analytics transformation design rather than dashboard layout, query debugging, ingestion, or ML serving.
2. If matched, activate lead agent `analytics-engineering-lead`.
3. If the request is only dashboard design, route away from this skill.
4. If orchestrated, defer to the orchestrating skill but preserve the deterministic `assets/` and `scripts/` contract.
