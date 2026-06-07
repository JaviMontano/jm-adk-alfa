---
name: ai-software-architecture-primary
type: execution
version: 2.1.0
description: "Execute the deterministic AI Software Architecture workflow."
triad:
  lead: "ai-software-architecture-lead"
  support: "ai-software-architecture-support"
  guardian: "ai-software-architecture-guardian"
---

# AI Software Architecture - Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|-----------|-------------|----------|-----------|
| `{{system_name}}` | System or product name | Yes | User input |
| `{{use_case}}` | AI-enabled workflow or decision | Yes | User input |
| `{{context}}` | Codebase notes, architecture notes, or constraints | Yes | User or repository |
| `{{constraints}}` | Risk, compliance, latency, availability, or rollout rules | No | User or guardrails |

## Execution Steps

1. Confirm activation against `SKILL.md`.
2. Read `assets/manifest.json` and required contract assets.
3. Load only the relevant references from `references/`.
4. Build evidence with `[EXPLICIT]`, `[INFERRED]`, and `[OPEN]` tags.
5. Produce the required report sections: system context, evidence, layers, components, patterns, quality scenarios, ADRs, debt, evolution, validation.
6. Run the Guardian checklist. If JSON handoff exists, validate it with `scripts/validate_ai_architecture_report.py`.
