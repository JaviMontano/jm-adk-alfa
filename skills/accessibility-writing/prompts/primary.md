---
name: accessibility-writing-primary
type: execution
version: 2.0.0
description: "Execute the Accessibility Writing workflow with copy, evidence, and claim-safety triad orchestration."
triad:
  lead: "accessibility-writing-lead"
  support: "accessibility-writing-support"
  guardian: "accessibility-writing-guardian"
---

# Accessibility Writing — Execute

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
3. **Lead** (`accessibility-writing-lead`): Execute SKILL.md Steps 1-4 for `{{task}}`
   - Identify content type, audience, locale, channel, constraints, and missing context
   - Produce reader-facing copy separately from validation notes
   - Rewrite alt text, links, instructions, errors, and body copy as applicable
   - Mark missing visual/chart/reading-level evidence as `not verified`
4. **Support** (`accessibility-writing-support`): Review for cross-cutting concerns
   - Meaning preservation, scannability, localization, inclusive language, and user recovery
5. **Guardian** (`accessibility-writing-guardian`): Validate
   - No invented visual details, reading-level guarantees, or unsupported claims
   - Evidence is outside final reader-facing copy unless requested inline
   - Related skill routing is correct for testing, design, or audit requests

## Output

- Accessible writing deliverable for `{{task}}` in `{{output_format}}`
- Final reader-facing copy
- Review table with original, issue, rewrite, rationale, assumptions, and status
- Confidence score based on source completeness and validation coverage
