---
name: user-prompt-filter-primary
type: execution
version: 2.1.0
description: "Execute deterministic prompt filtering before agent or tool execution."
triad:
  lead: "user-prompt-filter-lead"
  support: "user-prompt-filter-support"
  guardian: "user-prompt-filter-guardian"
---

# User Prompt Filter - Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|-----------|-------------|----------|-----------|
| `{{prompt}}` | Raw incoming user prompt | Yes | User input |
| `{{surface}}` | chat / agent / tool / shell / browser / mcp / hook / automation | Yes | User or context |
| `{{protected_assets}}` | Assets that must not be exposed or mutated | Yes | Context |
| `{{allowed_actions}}` | Permitted downstream actions | Yes | Context |

## Execution

1. Normalize the input into `assets/filter-input-schema.json`.
2. Classify against `assets/threat-taxonomy.json`.
3. Score with `assets/risk-scoring-policy.json`.
4. Sanitize with `assets/sanitization-policy.json`.
5. Return decision, evidence, sanitized prompt, constraints, and residual risk.
