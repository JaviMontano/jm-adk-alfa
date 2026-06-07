---
name: analytics-events-quick
type: variation
version: 2.0.0
description: "Analytics Events in quick mode."
---

# Analytics Events — quick Mode

## When to Use

Use quick mode for a compact but complete event taxonomy or tracking plan.

## Dynamic Parameters

| Parameter | Required | Filled By |
|-----------|----------|-----------|
| `{{task}}` | Yes | User input |
| `{{context}}` | No | Auto-detected |
| `{{depth}}` | No | Set to "quick" |

## Execution

1. Load `knowledge/body-of-knowledge.md` and `assets/analytics-events-contract.json`.
2. Produce only the essential taxonomy, events, properties, identity policy, tracking plan, and validation notes.
3. Keep assumptions explicit and do not skip evidence.
4. Guardian validates naming, properties, identity, tracking plan, privacy, and evidence checks.

## Output

- Compact tracking plan
- Evidence references and open gaps
- Validation checklist
