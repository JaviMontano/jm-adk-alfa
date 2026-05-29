---
name: accessibility-testing-primary
type: execution
version: 2.0.0
description: "Execute the Accessibility Testing workflow with evidence-first triad orchestration."
triad:
  lead: "accessibility-testing-lead"
  support: "accessibility-testing-support"
  guardian: "accessibility-testing-guardian"
---

# Accessibility Testing — Execute

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
3. **Lead** (`accessibility-testing-lead`): Execute SKILL.md Steps 1-4 for `{{task}}`
   - Define target scope and environment
   - Produce or run automated test commands when runnable
   - Build manual keyboard, screen reader, contrast, and motion evidence matrices
   - Mark every untested item as `not verified`
4. **Support** (`accessibility-testing-support`): Review for blind spots
   - Dynamic states, keyboard paths, AT smoke coverage, suppressions, and claim boundaries
5. **Guardian** (`accessibility-testing-guardian`): Validate
   - No unsupported WCAG conformance claim
   - Evidence tags complete
   - Pass/fail/conditional/not-verified statuses present
   - Suppressions and remediation boundaries are governed

## Output

- Accessibility testing report for `{{task}}` in `{{output_format}}`
- Exact commands, artifacts, and manual scripts where available
- Findings with user impact, recommended fix, owner suggestion, and retest criterion
- Not-verified areas and confidence score tied to evidence
