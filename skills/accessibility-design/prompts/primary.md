---
name: accessibility-design-primary
type: execution
version: 2.0.0
description: "Execute the Accessibility Design workflow with triad orchestration."
triad:
  lead: "accessibility-design-lead"
  support: "accessibility-design-support"
  guardian: "accessibility-design-guardian"
---

# Accessibility Design — Execute

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
3. **Lead** (`accessibility-design-lead`): Execute SKILL.md Steps 1-4 for `{{task}}`
   - Discover: feature/component scope, states, user journey, tokens, constraints
   - Analyze: native HTML vs ARIA, WCAG/POUR mapping, keyboard and focus model
   - Execute: accessible interaction spec or implementation guidance
   - Validate: acceptance criteria and validation matrix
4. **Support** (`accessibility-design-support`): Review for cross-cutting concerns
   - Content, forms/errors, reduced motion, responsive/zoom, design tokens, implementation constraints
5. **Guardian** (`accessibility-design-guardian`): Validate
   - Native HTML considered before ARIA
   - Keyboard map, focus plan, screen reader expectations, and contrast/token status are present
   - Acceptance criteria are testable
   - Audit/testing boundary is respected

## Output

- Accessible interaction spec or implementation guidance for `{{task}}` in `{{output_format}}`
- Evidence tags on every claim
- WCAG/POUR mapping, keyboard map, focus plan, semantic/ARIA decision log, validation matrix
- Confidence score (>= 0.95)
