---
name: accessibility-design-quick
type: variation
version: 2.0.0
description: "Accessibility Design in quick mode."
---

# Accessibility Design — quick Mode

## When to Use

Use quick mode for one small component or interaction.

## Dynamic Parameters

| Parameter | Required | Filled By |
|-----------|----------|-----------|
| `{{task}}` | Yes | User input |
| `{{context}}` | No | Auto-detected |
| `{{depth}}` | No | Set to "quick" |

## Execution

1. Load skill: `skills/accessibility-design/knowledge/body-of-knowledge.md`
2. Identify component, states, and user journey.
3. Produce native/ARIA decision, keyboard behavior, focus rule, content/error requirement, and validation checklist.
4. Mark missing contrast/runtime/SR evidence as not verified.
5. Keep audit/reporting requests routed to `accessibility-audit`.

## Output

- Compact accessible interaction spec
- Acceptance criteria and not-verified items
- No unsupported compliance claim
