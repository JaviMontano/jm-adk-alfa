---
name: prompt-engineering-primary
type: execution
version: 2.0.0
description: "Execute the Prompt Engineering workflow with triad orchestration."
triad:
  lead: "prompt-engineering-lead"
  support: "prompt-engineering-support"
  guardian: "prompt-engineering-guardian"
---

# Prompt Engineering - Execute

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
2. **Check assets**: Read `assets/pattern-decision-matrix.json` and `assets/prompt-engineering-checklist.md`
3. **Lead** (`prompt-engineering-lead`): Execute SKILL.md Steps 1-4 for `{{task}}`
   - Discover → Analyze → Execute → Validate
   - Apply evidence tags on all claims
4. **Support** (`prompt-engineering-support`): Review for cross-cutting concerns
   - Edge cases, security, accessibility, performance
5. **Guardian** (`prompt-engineering-guardian`): Validate
   - Evidence tags complete
   - Quality gate met
   - Constitution XIII + XIV respected
   - Prompt packet passes deterministic validation

## Output

- Prompt engineering packet for `{{task}}` in `{{output_format}}`
- Evidence tags on every claim
- Recommendations kept in a separate backlog section
- Validation result from `scripts/validate_prompt_packet.py` when JSON packet is produced
