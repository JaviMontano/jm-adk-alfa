---
name: environment-detection-quick
type: variation
version: 2.0.0
description: "Environment Detection in quick mode."
---

# Environment Detection — quick Mode

## When to Use

Use quick mode when the user needs a short startup decision and signals are unambiguous.

## Dynamic Parameters

| Parameter | Required | Filled By |
|-----------|----------|-----------|
| `{{task}}` | Yes | User input |
| `{{signals}}` | Yes | Local file/tool/model evidence |
| `{{depth}}` | No | Set to "quick" |

## Execution

1. List the top three signals.
2. Map IDE to triad mode.
3. Map context budget to tier or mark unknown.
4. Return one loading-plan table.
5. Flag any missing evidence.

## Output

- IDE, triad mode, model tier, confidence.
- Signal list with evidence tags.
- Conservative loading plan.
- Validation status.
