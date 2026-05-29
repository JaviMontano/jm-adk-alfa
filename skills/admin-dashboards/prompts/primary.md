---
name: admin-dashboards-primary
type: execution
version: 2.0.0
description: "Execute the Admin Dashboards workflow with evidence-first product, data, and authorization contracts."
triad:
  lead: "admin-dashboards-lead"
  support: "admin-dashboards-support"
  guardian: "admin-dashboards-guardian"
---

# Admin Dashboards — Execute

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
3. **Lead** (`admin-dashboards-lead`): Execute SKILL.md Steps 1-4 for `{{task}}`
   - Identify entities, workflows, data sources, roles, routes, actions, and states
   - Produce data contract, RBAC matrix, table contract, CRUD flows, metrics contract, and test plan
   - Mark missing APIs/schemas/metrics/realtime channels as `not verified`
4. **Support** (`admin-dashboards-support`): Review for cross-cutting concerns
   - Security, accessibility, performance, responsive density, export governance, auditability
5. **Guardian** (`admin-dashboards-guardian`): Validate
   - No invented backend, schema, KPI, permission, or realtime channel
   - RBAC includes backend enforcement or explicit `not verified`
   - Empty/loading/error/permission states are covered

## Output

- Admin dashboard spec or scoped implementation for `{{task}}` in `{{output_format}}`
- Evidence-tagged assumptions and `not verified` gaps
- Test plan and acceptance gates
- Confidence score based on source completeness and validation coverage
