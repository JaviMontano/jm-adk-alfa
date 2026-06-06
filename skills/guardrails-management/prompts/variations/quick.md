---
name: guardrails-management-quick
type: variation
version: 2.0.0
description: "Guardrails Management in quick mode."
---

# Guardrails Management — quick Mode

## When to Use

Use quick mode when you need adjusted depth for the Guardrails Management workflow.

## Dynamic Parameters

| Parameter | Required | Filled By |
|-----------|----------|-----------|
| `{{task}}` | Yes | User input |
| `{{context}}` | No | Auto-detected |
| `{{depth}}` | No | Set to "quick" |

## Execution

1. Load skill: `skills/guardrails-management/knowledge/body-of-knowledge.md`
2. Load assets: `assets/manifest.json`, `assets/rule-schema.json`, and
   `assets/storage-map.json`
3. Execute at quick depth with evidence tags, confirmation state, rule type,
   target file, duplicate review, and verifiable check
4. Lead → Support → Guardian validation
5. Run offline packet validation when JSON output is produced

## Output

- Deliverable calibrated to quick depth
- Evidence-tagged, Constitution-compliant
- Rule proposal/stored-rule packet, validation, and risks
