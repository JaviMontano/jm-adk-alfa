---
name: discovery-orchestration-primary
type: execution
version: 2.0.0
description: "Execute the Discovery Orchestration workflow with triad orchestration."
triad:
  lead: "discovery-orchestration-lead"
  support: "discovery-orchestration-support"
  guardian: "discovery-orchestration-guardian"
---

# Discovery Orchestration — Execute

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
   `assets/pipeline-schema.json`, `assets/gate-policy.json`,
   `assets/deliverable-policy.json`, `assets/dependency-policy.json`,
   `assets/status-taxonomy.json`, and `assets/report-contract.json`
3. **Check guardrails**: Read available guardrails when present
4. **Lead** (`discovery-orchestration-lead`): Execute SKILL.md Steps 1-4 for `{{task}}`
   - Discover → Analyze → Execute → Validate
   - Apply evidence tags on all claims
   - Build pipeline, phases, dependency graph, gates, deliverable register,
     blockers, validation, and risks
5. **Support** (`discovery-orchestration-support`): Review for cross-cutting concerns
   - Dependency cycles, missing gates, unvalidated deliverables, owner gaps,
     unsafe parallelism, and blocked transitions
6. **Guardian** (`discovery-orchestration-guardian`): Validate
   - Evidence tags complete
   - Quality gate met
   - Orchestration packet contract satisfied
   - Constitution XIII + XIV respected
   - Output exceeds expectations

## Output

- Primary deliverable for `{{task}}` in `{{output_format}}`
- Discovery orchestration packet with pipeline, phases, dependencies, gates,
  deliverables, blockers, validation, risks, and confidence score
