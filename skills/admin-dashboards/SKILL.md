---
name: admin-dashboards
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Build admin dashboard interfaces with data tables, filters, charts, CRUD
  operations, real-time data updates, RBAC, auditability, and operational UI
  states. Covers layout patterns, data contracts, state management, and
  safety gates. [EXPLICIT]
  Trigger: "admin panel", "dashboard", "data table", "CRUD interface",
  "back-office", "RBAC dashboard", "admin console"
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

Guides the architecture and implementation of admin dashboard interfaces featuring sortable/filterable data tables, CRUD operations, charts/metrics, real-time updates, audit trails, empty/loading/error states, responsive dense layouts, and role-based access control enforced beyond the UI. Use when building back-office tools, content management systems, or operational dashboards. Do not invent APIs, schemas, metrics, permissions, or realtime channels without repo evidence or explicit user input. [EXPLICIT]

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

- Loading all records client-side instead of server-side pagination
- Building custom data tables from scratch when libraries like TanStack Table exist
- Hiding menu items but not protecting API routes for unauthorized roles
- Inventing `/api/*`, Firestore collections, WebSocket/SSE channels, or KPI formulas without evidence
- Treating admin dashboards as marketing pages instead of dense operational tools
- Logging full sensitive payloads in audit trails
- Exporting raw PII or spreadsheet formulas without governance
- Reporting performance targets without dataset and measurement context

## Related Skills

- `firestore-queries` — efficient data fetching for dashboard tables
- `cloud-functions` — API endpoints backing CRUD operations

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

## Assets

- `assets/deliverable-checklist.md` provides the reusable checklist for final deliverable and guardian review.
