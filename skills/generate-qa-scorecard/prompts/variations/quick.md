---
name: generate-qa-scorecard-quick
type: execution
version: 2.0.0
description: "Fast QA scorecard generation with deterministic math checks."
---

# Quick QA Scorecard

Use when the user provides dimension-level findings and needs a compact
executive scorecard.

## Steps

1. Confirm all 7 dimensions are present or marked `na`.
2. Apply strict status and point rules.
3. Calculate total, evaluated maximum, percentage, and grade.
4. Rank at most 3 priority actions.
5. Block delivery if math, grade, or action ranking does not match policy.

## Output

- Score table
- Grade line
- Top 3 actions
- Guardian decision
