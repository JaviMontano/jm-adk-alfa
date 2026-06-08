---
name: generate-qa-scorecard-primary
type: execution
version: 2.0.0
description: "Execute deterministic executive QA scorecard generation."
triad:
  lead: "generate-qa-scorecard-lead"
  support: "generate-qa-scorecard-support"
  guardian: "generate-qa-scorecard-guardian"
---

# Generate QA Scorecard - Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|-----------|-------------|----------|-----------|
| `{{findings}}` | Dimension-level critical, warning, and info counts | Yes | User or audit artifacts |
| `{{plugin}}` | Plugin or component being scored | Yes | User input |
| `{{scope}}` | Evaluated dimensions and unavailable evidence | No | User or audit artifacts |
| `{{output_format}}` | md or json | No | Auto |

## Execution

1. Load `knowledge/body-of-knowledge.md`.
2. Load assets under `assets/` and apply policies in this order: contract,
   dimensions, scoring, grade, actions, evidence.
3. Lead: map evidence to all 7 dimensions and calculate score.
4. Support: challenge missing dimensions, status mismatches, math errors,
   undisclosed reduced scope, and weak actions.
5. Guardian: block output if any dimension is absent, score math is wrong, grade
   threshold is wrong, or priority actions are out of order.

## Output

- Evidence Summary
- Scorecard
- Grade
- Top 3 Priority Actions
- Reduced Scope
- Guardian Decision
