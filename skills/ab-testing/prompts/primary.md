---
name: ab-testing-primary
type: execution
version: 2.0.0
description: "Execute the Ab Testing workflow with triad orchestration."
triad:
  lead: "ab-testing-lead"
  support: "ab-testing-support"
  guardian: "ab-testing-guardian"
---

# Ab Testing — Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|-----------|-------------|----------|-----------|
| `{{task}}` | What to accomplish | Yes | User input |
| `{{context}}` | Background and constraints | Yes | User or codebase |
| `{{constraints}}` | Additional rules | No | Guardrails JSON |
| `{{depth}}` | quick / standard / deep | No | Auto |
| `{{output_format}}` | html / docx / xlsx / md | No | Auto |

## Execution

1. **Load knowledge**: Read `knowledge/body-of-knowledge.md`
2. **Check guardrails**: Read `references/guardrails/*.json`
3. **Lead** (`ab-testing-lead`): Execute SKILL.md Steps 1-4 for `{{task}}`
   - Discover: goal, decision, audience, variants, metrics, traffic, constraints
   - Analyze: test readiness, sample-size assumptions, duration, and validity threats
   - Execute: experiment brief or review verdict
   - Validate: decision rule, evidence tags, and open requirements
4. **Support** (`ab-testing-support`): Review cross-cutting risks
   - Analytics instrumentation, guardrail metrics, sample ratio mismatch,
     peeking, seasonality, overlapping experiments, and segment bias
5. **Guardian** (`ab-testing-guardian`): Validate
   - Evidence tags complete
   - Quality gate met
   - Constitution XIII + XIV respected
   - No significance, ROI, or causality claim is made without required data

## Output

- Experiment brief or review verdict for `{{task}}` in `{{output_format}}`
- Evidence tags on every claim
- Launch checklist, decision rule, risks, and open requirements
- Confidence score (>= 0.95)
