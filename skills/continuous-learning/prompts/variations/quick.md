---
name: continuous-learning-quick
type: variation
version: 2.0.0
description: "Continuous Learning in quick mode."
---

# Continuous Learning — quick Mode

## When to Use

Use quick mode after a single clear debate or discovery where no amendment
candidate is expected.

## Dynamic Parameters

| Parameter | Required | Filled By |
|-----------|----------|-----------|
| `{{task}}` | Yes | User input |
| `{{context}}` | No | Auto-detected |
| `{{depth}}` | No | Set to "quick" |

## Execution

1. Search the relevant `insights/` domain file.
2. Capture answer, refined question, and coverage gaps.
3. Draft one insight candidate or a duplicate/refinement decision.
4. Validate required fields before delivery.

## Output

- One insight candidate or duplicate decision
- Evidence-tagged update plan
- Guardian pass/block
