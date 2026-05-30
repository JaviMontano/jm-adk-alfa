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

0. **Routing gate**: Run SKILL.md "Routing Gate". If this is a public/marketing page or pure backend authoring, route away and stop. Otherwise set `{{depth}}` (quick/standard/deep) and write-vs-analysis mode.
1. **Load knowledge**: Read `knowledge/body-of-knowledge.md` — use its contract tables as the field schema.
2. **Check guardrails**: Read `references/guardrails/*.json` if present; otherwise apply the SKILL.md anti-pattern table as guardrails.
3. **Inventory (Lead)**: Grep the repo for existing routes, table/chart/form libs, API clients, auth middleware/rules, and schemas before designing anything. Reuse before adding.
4. **Lead** (`admin-dashboards-lead`): Execute SKILL.md Steps 1-4 for `{{task}}`.
   - Inventory entities, workflows, data sources, roles, routes, actions, and states.
   - Produce the nine contracts (data, RBAC, table, CRUD, metrics, realtime, audit, export, state) plus a test plan with negative cases.
   - Mark missing APIs/schemas/metrics/realtime channels as `not verified` — never infer them.
   - Pull in `admin-dashboards-specialist` for any panel with large data, destructive/bulk actions, complex RBAC, charts, realtime, or exports.
5. **Support** (`admin-dashboards-support`): Adversarial review for blind spots and dependencies.
   - Authorization gaps (IDOR, deep-link), destructive reach, state holes, export/audit leakage, a11y/responsive/perf claims, invented backend.
   - Return a prioritized defect list (blocker / should-fix / note).
6. **Guardian** (`admin-dashboards-guardian`): Validate the hard gates.
   - No invented backend, schema, KPI, permission, or realtime channel.
   - RBAC includes backend enforcement or explicit `not verified`; full state matrix covered; destructive flows recoverable and audited.
   - On any miss return `status: degraded` with the failed gate and next action.

## Output

- Admin dashboard spec or scoped implementation for `{{task}}` in `{{output_format}}` (mirror `examples/example-output.md` section structure when producing a spec).
- Evidence-tagged claims; `[ASSUMPTION]` / `not verified` for every uncited backend fact.
- Test plan with negative/authorization cases and acceptance gates.
- Confidence score, explicitly capped by unresolved `not verified` items.
