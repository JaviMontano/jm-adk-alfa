---
name: ai-assisted-testing-deep
type: variation
version: 2.0.0
description: "Ai Assisted Testing — deep analysis mode. Exhaustive coverage."
---

# AI Assisted Testing — Deep Mode

## When to Use

Use deep mode for high-risk modules, security-sensitive inputs, parsers, payment logic, auth, or production regressions.

## Dynamic Parameters

| Parameter | Required | Filled By |
|-----------|----------|-----------|
| `{{task}}` | Yes | User input |
| `{{context}}` | Yes | User + codebase scan |
| `{{depth}}` | No | Set to "deep" |

## Execution (Deep)

1. Map requirements, code paths, current tests, coverage, and defects.
2. Generate unit, property, fuzz, mutation, and regression candidates.
3. Include boundary values, negative paths, and invariant checks.
4. Produce JSON plan for offline validation.

## Output

- Full evidence-backed test plan.
- Coverage and risk map.
- Bounded fuzzing and mutation plan.
- Validation evidence.
