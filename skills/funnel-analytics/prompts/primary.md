---
name: funnel-analytics-primary
type: execution
version: 2.0.0
description: "Execute the Funnel Analytics workflow with measurement-first triad orchestration."
triad:
  lead: "funnel-analytics-lead"
  support: "funnel-analytics-support"
  guardian: "funnel-analytics-guardian"
---

# Funnel Analytics - Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|-----------|-------------|----------|-----------|
| `{{task}}` | Funnel analysis or tracking-plan objective | Yes | User input |
| `{{context}}` | Events, counts, dashboards, code, docs, or constraints | Yes | User or codebase |
| `{{constraints}}` | Additional rules | No | Guardrails JSON |
| `{{depth}}` | quick / standard / deep | No | Auto |
| `{{output_format}}` | html / docx / xlsx / md | No | Auto |

## Execution

1. **Load knowledge**: Read `knowledge/body-of-knowledge.md`
2. **Load assets**: Read `assets/deliverable-checklist.md`
3. **Check guardrails**: Read `references/guardrails/*.json` when present
4. **Lead** (`funnel-analytics-lead`): Execute SKILL.md Steps 1-4 for `{{task}}`
   - Discover -> Analyze -> Execute -> Validate
   - Apply evidence tags to all claims
5. **Support** (`funnel-analytics-support`): Review for cross-cutting concerns
   - Units, windows, identity stitching, data quality, privacy, and segment risk
6. **Guardian** (`funnel-analytics-guardian`): Validate
   - Evidence tags complete
   - No invented metrics, events, or causality
   - Asset checklist met
   - Quality gate satisfied

## Output

- Primary deliverable for `{{task}}` in `{{output_format}}`
- Evidence tags on every claim
- Recommendations separated by evidence strength
- Residual risks and `not verified` gaps
