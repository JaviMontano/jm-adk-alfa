---
name: ai-workflow-automation-primary
type: execution
version: 2.0.0
description: "Execute the Ai Workflow Automation workflow with triad orchestration."
triad:
  lead: "ai-workflow-automation-lead"
  support: "ai-workflow-automation-support"
  guardian: "ai-workflow-automation-guardian"
---

# AI Workflow Automation — Execute

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
   `assets/workflow-schema.json`, `assets/actor-taxonomy.json`,
   `assets/approval-gate-policy.json`, `assets/handoff-policy.json`,
   `assets/failure-policy.json`, and `assets/report-contract.json`
3. **Check guardrails**: Read available `references/guardrails/*.json` files
   when present
4. **Lead** (`ai-workflow-automation-lead`): Execute SKILL.md Steps 1-4 for `{{task}}`
   - Discover → Analyze → Execute → Validate
   - Apply evidence tags on all claims
   - Define actor map, step graph, approval gates, handoffs, fallbacks, and
     validation checks
5. **Support** (`ai-workflow-automation-support`): Review for cross-cutting concerns
   - Missing approvals, unbounded retries, weak AI output contracts, handoff
     gaps, security, accessibility, and operational edge cases
6. **Guardian** (`ai-workflow-automation-guardian`): Validate
   - Evidence tags complete
   - Quality gate met
   - Workflow plan contract satisfied
   - Constitution XIII + XIV respected
   - Output exceeds expectations

## Output

- Primary deliverable for `{{task}}` in `{{output_format}}`
- Workflow plan with actor map, steps, approval gates, handoffs, retries,
  fallbacks, validation evidence, risks, and confidence score
