---
name: funnel-analytics-quick
type: variation
version: 2.0.0
description: "Funnel Analytics in quick mode."
---

# Funnel Analytics - Quick Mode

## When to Use

Use quick mode when the user needs a fast funnel sanity check, tracking gap list, or next-step brief from limited evidence.

## Dynamic Parameters

| Parameter | Required | Filled By |
|-----------|----------|-----------|
| `{{task}}` | Yes | User input |
| `{{context}}` | No | Auto-detected |
| `{{depth}}` | No | Set to "quick" |

## Execution

1. Load skill: `skills/funnel-analytics/knowledge/body-of-knowledge.md`
2. Load `assets/deliverable-checklist.md`
3. Check guardrails: `references/guardrails/*.json` when present
4. Produce a compact scope, funnel definition, gaps, and next actions
5. Lead -> Support -> Guardian validation

## Output

- Compact report calibrated to quick depth
- Evidence-tagged facts and `not verified` gaps
- Measurement-first next actions
