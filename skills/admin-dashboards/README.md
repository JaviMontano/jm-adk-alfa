# Admin Dashboards

Build or specify operational admin dashboards with tables, filters, charts, CRUD workflows, RBAC, audit trails, responsive dense layouts, and safe data handling.

## Triggers

- "admin dashboard"
- "admin panel"
- "back-office"
- "CRUD interface"
- "data table"
- "RBAC dashboard"
- "operations dashboard"
- "management console"

## Allowed Tools

- Read
- Write
- Glob
- Grep
- Bash

## Quick Use

Use this skill when the user needs a working admin experience or an implementation-ready spec for operational users. It should produce contracts for data, permissions, states, workflows, UI structure, and validation before or during implementation.

Minimum useful input:

- entities and data sources;
- roles, permissions, and backend enforcement location;
- table fields, filters, sorting, pagination, and bulk actions;
- CRUD workflows and destructive-action rules;
- metrics/charts with formulas, owners, time range, timezone, and freshness;
- realtime requirements and acceptable fallback;
- export needs, PII boundaries, audit rules, and responsive constraints.

If backend APIs, schemas, RBAC rules, metrics, or realtime channels are missing, mark them `not verified` instead of inventing them.

## Output Format

Markdown spec with:

- scope and assumptions;
- entity/data contract;
- RBAC matrix;
- navigation and layout;
- table behavior contract;
- CRUD and bulk action workflows;
- metrics/charts contract;
- realtime and refresh strategy;
- empty/loading/error/permission states;
- security, audit, export, accessibility, responsive, and performance gates;
- test plan and not-verified items.
