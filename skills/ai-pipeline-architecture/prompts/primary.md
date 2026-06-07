---
name: ai-pipeline-architecture-primary
type: execution
version: 2.1.0
description: "Execute deterministic AI pipeline architecture workflow."
triad:
  lead: "ai-pipeline-architecture-lead"
  support: "ai-pipeline-architecture-support"
  guardian: "ai-pipeline-architecture-guardian"
---

# AI Pipeline Architecture - Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|-----------|-------------|----------|-----------|
| `{{system}}` | AI system or project name | Yes | User input |
| `{{context}}` | Data, model, serving, compliance, and team constraints | Yes | User or repo scan |
| `{{mode}}` | greenfield / modernization / audit | No | Auto |
| `{{scope}}` | executive / technical | No | Auto |

## Execution

1. Load `SKILL.md`, `references/*.md`, and `assets/*.json`.
2. Build evidence ids before decisions.
3. Produce development and production pipeline stages.
4. Select data stores with workload rationale.
5. Define registry, CI/CD gates, and AP/NF/SEC/CP requirements.
6. Validate the packet offline before delivery.
