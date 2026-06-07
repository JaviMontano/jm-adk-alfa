---
name: ai-testing-strategy-primary
type: execution
version: 2.1.0
description: "Execute the deterministic AI Testing Strategy workflow."
triad:
  lead: "ai-testing-strategy-lead"
  support: "ai-testing-strategy-support"
  guardian: "ai-testing-strategy-guardian"
---

# AI Testing Strategy - Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|-----------|-------------|----------|-----------|
| `{{system_name}}` | System or product name | Yes | User input |
| `{{use_case}}` | AI-enabled workflow or decision | Yes | User input |
| `{{context}}` | Codebase notes, testing stack, monitoring stack, or constraints | Yes | User or repository |
| `{{constraints}}` | Risk, compliance, privacy, latency, fairness, or automation rules | No | User or guardrails |

## Execution Steps

1. Confirm activation against `SKILL.md`.
2. Read `assets/manifest.json` and required contract assets.
3. Load only relevant references from `references/`.
4. Build evidence with `[EXPLICIT]`, `[INFERRED]`, and `[OPEN]` tags.
5. Produce the required report sections: system context, evidence, matrix coverage, model tests, data quality tests, fairness/compliance tests, integration, automation gates, monitoring, validation.
6. Run the Guardian checklist. If JSON handoff exists, validate it with `scripts/validate_ai_testing_strategy.py`.
