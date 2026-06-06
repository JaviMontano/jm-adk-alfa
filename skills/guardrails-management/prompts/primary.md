---
name: guardrails-management-primary
type: execution
version: 2.0.0
description: "Execute the Guardrails Management workflow with triad orchestration."
triad:
  lead: "guardrails-management-lead"
  support: "guardrails-management-support"
  guardian: "guardrails-management-guardian"
---

# Guardrails Management — Execute

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
   `assets/rule-schema.json`, `assets/classification-policy.json`,
   `assets/confirmation-policy.json`, `assets/conflict-policy.json`,
   `assets/storage-map.json`, and `assets/report-contract.json`
3. **Check guardrails**: Read available `references/guardrails/*.json` files
   when present
4. **Lead** (`guardrails-management-lead`): Execute SKILL.md Steps 1-4 for `{{task}}`
   - Discover → Analyze → Execute → Validate
   - Apply evidence tags on all claims
   - Never store unconfirmed proposals
5. **Support** (`guardrails-management-support`): Review for cross-cutting concerns
   - Duplicate rules, conflicts, wrong target file, unverifiable checks, and
     missing deactivation audit trail
6. **Guardian** (`guardrails-management-guardian`): Validate
   - Evidence tags complete
   - Quality gate met
   - Operation packet contract satisfied
   - Constitution XIII + XIV respected
   - Output exceeds expectations

## Output

- Primary deliverable for `{{task}}` in `{{output_format}}`
- Rule proposal or stored rule packet, confirmation state, conflict review,
  storage action, validation evidence, risks, and confidence score
