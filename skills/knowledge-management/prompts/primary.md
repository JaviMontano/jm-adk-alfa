---
name: knowledge-management-primary
type: execution
version: 2.0.0
description: "Execute the Knowledge Management workflow with triad orchestration."
triad:
  lead: "knowledge-management-lead"
  support: "knowledge-management-support"
  guardian: "knowledge-management-guardian"
---

# Knowledge Management — Execute

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
2. **Load deterministic assets**: Read `assets/manifest.json`,
   `assets/knowledge-taxonomy.json`, `assets/searchability-policy.json`,
   `assets/freshness-policy.json`, and `assets/report-contract.json`
3. **Check guardrails**: Read available guardrails only when present
4. **Lead** (`knowledge-management-lead`): Execute SKILL.md Steps 1-4 for `{{task}}`
   - Discover → Analyze → Execute → Validate
   - Apply evidence tags on all register claims
   - Use explicit report `reference_date` for decay decisions
5. **Support** (`knowledge-management-support`): Review for cross-cutting concerns
   - Searchability gaps, stale entries, orphan owners, duplicate sources,
     contradictions, and handoff risks
6. **Guardian** (`knowledge-management-guardian`): Validate
   - Evidence tags complete
   - Quality gate met
   - Report contract satisfied
   - Constitution XIII + XIV respected
   - Output exceeds expectations

## Output

- Primary deliverable for `{{task}}` in `{{output_format}}`
- Evidence tags on every claim
- Knowledge register, searchability map, decay review, action log, validation,
  risks, and confidence score
