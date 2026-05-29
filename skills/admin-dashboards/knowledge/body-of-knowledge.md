# Admin Dashboards — Body of Knowledge

## Canon

Admin dashboards are dense operational tools. They prioritize repeated work, data correctness, authorization, recoverability, and scanability over marketing-style presentation. The skill must produce either an implementation-ready spec or a scoped patch, with explicit evidence for APIs, schemas, metrics, permissions, and realtime channels.

## Core Contracts

| Contract | Required fields | Failure mode to avoid |
| --- | --- | --- |
| Data contract | entity, source, endpoint/query, params, response shape, error shape, owner, freshness | Invented API paths or silent schema assumptions |
| RBAC contract | role, route, resource, action, UI visibility, backend enforcement, negative test | Hiding buttons without API authorization |
| Table contract | columns, sort, filters, search, pagination, selection, bulk actions, URL state | Loading all records client-side |
| CRUD contract | create/edit/delete flow, validation, optimistic behavior, rollback, conflict handling | Happy-path-only forms |
| Metrics contract | formula, unit, source, owner, date range, timezone, refresh rate | KPI cards with undefined calculations |
| Realtime contract | channel, event shape, freshness target, fallback, stale state | Assuming WebSocket/Firestore/SSE without evidence |
| Audit contract | actor, action, entity, timestamp, correlation ID, before/after summary, retention | Logging secrets or full sensitive payloads |
| Export contract | fields, filters applied, PII policy, CSV formula neutralization, permission | Raw PII export or spreadsheet injection |
| State contract | empty, loading, partial error, permission denied, conflict, timeout, offline, stale | Blank screens and unrecoverable errors |

## Quality Metrics
| Metric | Target | How to Measure |
|--------|--------|---------------|
| Backend evidence | 100% or `not verified` | APIs/schemas/policies are cited or marked as assumptions |
| RBAC coverage | 100% critical actions | Role x resource x action matrix has UI and API enforcement |
| Table scalability | Explicit target | Dataset size, pagination/virtualization, debounce, abort stale requests |
| State coverage | 100% critical panels | Empty/loading/error/permission/stale states specified |
| CRUD recoverability | 100% destructive flows | Confirmation, rollback/retry, conflict handling, audit trail |
| Metric integrity | 100% KPI cards | Formula, unit, source, time range, timezone, owner |
| Accessibility | 100% critical flows | Keyboard path, labels, aria-sort, focus trap, error association |
| Security | 100% risky paths | Escaping, authorization, IDOR checks, export sanitization |

## Design Rules

- Use dense but organized layouts; avoid landing-page hero patterns.
- Prefer server-side pagination for large datasets; use virtualization only when the full dataset is intentionally in the client.
- Preserve state in URL/query for operational handoff when useful.
- Use clear default filters and saved views for repeated workflows.
- Show partial data with explicit stale/error states rather than hiding entire dashboards.
- Confirm destructive and bulk actions with exact affected count.
- Keep audit logs useful without storing unnecessary PII or secrets.
- Use accessible tables: semantic headers, `aria-sort` where applicable, keyboard focus, visible selected rows, and announced errors.
- Treat realtime as a requirement with fallback, not a default.

## References
- Existing repo components, routes, APIs, schemas, rules, middleware, lockfiles, and design tokens.
- Related skills: `api-design`, `api-security`, `audit-trail-design`, `accessibility-testing`, `data-visualization`, `form-engineering`, `e2e-testing`.
