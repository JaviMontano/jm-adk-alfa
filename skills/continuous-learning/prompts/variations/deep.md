---
name: continuous-learning-deep
type: variation
version: 2.0.0
description: "Continuous Learning — deep analysis mode. Exhaustive coverage."
---

# Continuous Learning — Deep Mode

## When to Use

Use deep mode for repeated ambiguity, governance changes, or high-impact
decisions where amendment candidacy is plausible.

## Dynamic Parameters

| Parameter | Required | Filled By |
|-----------|----------|-----------|
| `{{task}}` | Yes | User input |
| `{{context}}` | Yes | User + codebase scan |
| `{{depth}}` | No | Set to "deep" |

## Execution (Deep)

1. Read source event and all relevant domain insight entries.
2. Build recurrence evidence and duplicate map.
3. Extract reusable patterns, refined questions, and coverage gaps.
4. Draft update plan and amendment candidates when threshold is met.
5. Validate report with `scripts/check.sh`.

## Output

- Learning report with recurrence evidence and duplicate analysis
- Insight update plan
- Amendment decision with rationale
- Guardian validation
