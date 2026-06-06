---
name: ai-assisted-testing-quick
type: variation
version: 2.0.0
description: "Ai Assisted Testing in quick mode."
---

# AI Assisted Testing — Quick Mode

## When to Use

Use quick mode for small modules or a short candidate-test list.

## Dynamic Parameters

| Parameter | Required | Filled By |
|-----------|----------|-----------|
| `{{task}}` | Yes | User input |
| `{{context}}` | No | Auto-detected |
| `{{depth}}` | No | Set to "quick" |

## Execution

1. Identify targets and evidence.
2. Return top candidate tests with oracles.
3. Include missing coverage and risks.
4. Avoid fuzzing/mutation unless bounds are known.

## Output

- Compact test plan.
- Proposed execution status.
- Missing evidence and next validation command.
