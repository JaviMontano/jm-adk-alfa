---
name: admin-dashboards
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Architect and implement back-office admin dashboards: dense data tables
  (server-side sort/filter/search/pagination, bulk actions, saved views),
  CRUD with conflict/rollback handling, KPI cards and charts, realtime/polling,
  RBAC enforced on UI and backend, audit trails, exports, and the full
  empty/loading/error/permission/stale state matrix. Produces an
  evidence-first spec or scoped patch; never invents APIs, schemas, KPI
  formulas, permissions, or realtime channels without repo evidence. [EXPLICIT]
  USE WHEN the deliverable is an internal operational UI driven by structured
  data and roles. DO NOT USE for public/marketing landing pages or decorative
  charts (route to landing/brand/data-visualization skills), nor for pure
  backend API or auth-policy authoring (route to api-design / api-security).
  Boundary: this skill owns the operator-facing surface and its data/RBAC
  contracts; it consumes — not authors — backend endpoints and policies.
  Trigger: "admin panel", "admin dashboard", "data table", "back-office",
  "RBAC dashboard", "admin console", "CRUD interface", "internal tool"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Admin Dashboards

> "A dashboard should answer questions before they're asked." — Stephen Few

## TL;DR

Architects and implements admin/back-office UIs: filterable/sortable data tables, CRUD with recovery, KPI cards and charts, realtime updates, audit trails, exports, the full state matrix, dense responsive layouts, and RBAC enforced beyond the UI. Output is an evidence-tagged spec or scoped patch. The non-negotiable rule: do not invent APIs, schemas, metrics, permissions, or realtime channels — cite repo evidence or mark `not verified`. [EXPLICIT]

## Routing Gate (run first)

Before any work, classify the request to avoid misroute and pick depth:

- **Is it an operator-facing tool over structured data + roles?** If no (public/marketing page, decorative chart) → stop and route to landing/brand/`data-visualization`. If the ask is pure backend endpoint or auth-policy authoring → route to `api-design` / `api-security`; this skill consumes those contracts.
- **Depth:** `quick` when APIs, RBAC, states, and acceptance are already known and the change is small and non-destructive. `deep` for new dashboards, sensitive data, destructive/bulk actions, exports, unclear RBAC, large datasets, or realtime. Otherwise `standard`.
- **Write vs analysis-only:** if the user asks for a design/spec, do not mutate files even when Write/Bash are allowed.

## Procedure

### Step 1: Discover
- Identify data entities and their relationships (users, orders, content, settings)
- Review user roles and permission levels (admin, editor, viewer)
- Check existing API endpoints and data schemas
- Determine real-time requirements (WebSocket, polling, SSE)
- Capture operational workflows: list, inspect, create, update, delete, bulk actions, export, audit, and recovery
- Mark missing backend, schema, permission, metric, or endpoint evidence as `[ASSUMPTION]` or `not verified`

### Step 2: Analyze
- Plan navigation structure (sidebar, breadcrumbs, nested routes)
- Design data table features (sort, filter, search, pagination, bulk actions)
- Choose chart library (Chart.js, Recharts, D3, Apache ECharts)
- Evaluate state management for complex filter/table interactions
- Define RBAC matrix: role x route x action x resource x backend enforcement point
- Define data contract: endpoint/query, parameters, pagination, sorting, filters, response shape, error shape, freshness, and owner
- Define state contract: empty, loading, partial error, permission denied, stale data, conflict, timeout, offline, and retry
- Define audit contract for create/update/delete/export and destructive actions

### Step 3: Execute
- Build sidebar layout with collapsible navigation and role-based menu items
- Implement data tables with server-side pagination, sorting, and column configuration
- Add CRUD forms with validation, optimistic updates, and confirmation dialogs
- Create metric cards and charts for KPI overview section
- Wire real-time updates via Firestore listeners or WebSocket connections
- Add export functionality (CSV, PDF) for table data
- Prefer established table/chart/form libraries already present in the repo; if none exist, document the selection rationale before adding dependencies
- Treat destructive operations and bulk actions as confirmable, auditable workflows with rollback or recovery notes
- Sanitize rendered cell content and exports; prevent formula injection in CSV-style outputs
- Preserve URL/query state for filters, search, sort, pagination, and selected views when useful

### Step 4: Validate
- Test with large datasets (1000+ rows) — no UI freezing
- Verify CRUD operations handle errors gracefully (network failures, conflicts)
- Confirm role-based access hides unauthorized actions, not just routes
- Check keyboard navigation for data tables and forms
- Verify backend/API authorization or mark RBAC as `not verified`; hiding buttons is not enough
- Verify empty/loading/error/permission-denied states for each critical panel
- Verify KPI formulas, units, time ranges, timezone, freshness, and data owner before presenting metrics as truth
- Verify responsive density across mobile, tablet, and desktop without losing critical actions

## Quality Criteria

- [ ] Data tables handle sorting, filtering, and pagination without full page reload
- [ ] CRUD operations show loading states, success feedback, and error recovery
- [ ] Dashboard performance targets include measurement context, dataset size, and environment
- [ ] Role-based access enforced on both UI and API levels, or explicitly marked `not verified`
- [ ] Authorization matrix, data contract, state matrix, and audit trail are documented
- [ ] Exports protect PII and neutralize spreadsheet formula injection risks
- [ ] Empty, loading, error, offline, stale, and permission states are designed
- [ ] Responsive and keyboard-accessible flows are covered
- [ ] Evidence tags applied to all claims

## Anti-Patterns

| Anti-pattern | Why it fails | Correct move |
|--------------|--------------|--------------|
| Load all records client-side | Freezes UI past a few thousand rows; leaks unfiltered data | Server-side pagination; virtualize only when the full set is intentionally client-held |
| Hand-roll the table from scratch | Reimplements sort/filter/a11y bugs | Reuse a repo-present table lib (e.g. TanStack Table); document the choice if adding one |
| Hide the button but leave the API open | RBAC bypassed by deep-link or direct call | Enforce on backend; UI visibility is cosmetic; add a negative test |
| Invent `/api/*`, collections, channels, or KPI formulas | Silent fiction passed off as a contract | Cite repo evidence or mark `not verified` |
| Ship marketing-style hero layout | Wastes density operators need | Dense, scannable, repeated-work-first layout |
| Log full payloads / secrets in audit | Audit becomes a breach surface | Log actor, action, entity, before/after summary, correlation ID; minimize PII |
| Export raw PII or live spreadsheet formulas | Data leak + CSV/formula injection | Apply PII policy by role; neutralize `=+-@` formula prefixes |
| Quote a perf target with no context | Unfalsifiable claim | State dataset size, environment, and measurement method |

## Related Skills

- `api-design` — authoring/inspecting the endpoints this dashboard consumes
- `api-security` — backend authorization and IDOR checks behind RBAC
- `audit-trail-design` — actor/action/correlation audit schemas
- `form-engineering` — CRUD validation, optimistic updates, conflict UX
- `accessibility-testing` — keyboard, `aria-sort`, focus-trap verification
- `data-visualization` — chart data contracts and KPI rendering

## Usage

Example invocations:

- "/admin-dashboards" — Run the full admin dashboards workflow
- "admin dashboards on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Uses the language of the user request unless repo conventions require otherwise [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Does not certify backend authorization unless policies, middleware, rules, or endpoint checks were inspected or provided [EXPLICIT]
- Does not create or mutate files when the user asks for design/spec only [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
