# Example Output

## Scope and Assumptions

| Field | Value |
| --- | --- |
| Objective | Internal CRM admin dashboard spec |
| Users / roles | viewer, editor, admin |
| Entities | customers, orders, support tickets |
| Data sources | Customers REST API verified by user; orders/tickets not verified |
| Not verified | Orders API, tickets API, KPI formulas, timezone, realtime channel |

## Entity and Data Contract

| Entity | Source | Query / endpoint | Params | Response | Error shape | Owner | Freshness |
| --- | --- | --- | --- | --- | --- | --- | --- |
| customers | REST | `not verified: use documented customers endpoint` | status, owner, date, search, page, pageSize, sort | customer list + total count | validation, 403, 409, timeout | CRM team | request-time |
| orders | not verified | `not verified` | `por_confirmar` | `por_confirmar` | `por_confirmar` | `por_confirmar` | `por_confirmar` |
| support tickets | not verified | `not verified` | `por_confirmar` | `por_confirmar` | `por_confirmar` | Support team | realtime requested but not verified |

## Authorization Matrix

| Role | Route | Resource | Action | UI behavior | Backend enforcement | Negative test |
| --- | --- | --- | --- | --- | --- | --- |
| viewer | `/admin/customers` | customer | read | visible | not verified | viewer cannot call create/update/delete endpoint |
| editor | `/admin/customers/:id/edit` | customer | update | visible | not verified | editor receives 403 on delete |
| admin | `/admin/customers/:id/delete` | customer | delete | visible with confirmation | not verified | non-admin direct request returns 403 |

## Table Behavior Contract

| Table | Columns | Sort | Filters | Search | Pagination | Selection / bulk | URL state |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Customers | name, email, status, owner, last order, created | server-side | status, owner, date | debounced email search | server-side page/pageSize | bulk owner reassignment with exact count confirmation | persist filters/sort/page in query string |

## CRUD and Bulk Workflows

| Workflow | Validation | Loading / disabled states | Success | Error / conflict | Audit | Recovery |
| --- | --- | --- | --- | --- | --- | --- |
| Create customer | required fields and email format | disable submit while pending | toast + row inserted/refetched | show field errors or retry | actor/action/entity/timestamp | keep draft values |
| Delete customer | admin only + exact name confirmation | disable confirm while pending | remove row after success | 403/409/timeout handled | actor/action/entity/before summary/correlation ID | no optimistic delete unless backend supports restore |

## Metrics and Charts

| KPI / chart | Formula | Source | Unit | Time range / timezone | Refresh | Empty/error state |
| --- | --- | --- | --- | --- | --- | --- |
| Active customers | not verified | customers API | count | timezone not verified | on load/refetch | show not verified formula |
| Overdue tickets | not verified | tickets API not verified | count | timezone not verified | not verified | hide value until source exists |
| Monthly order volume | not verified | orders API not verified | count | month/timezone not verified | not verified | show setup required |

## Realtime and Refresh Strategy

Ticket realtime is requested but no WebSocket, SSE, Firestore, or polling channel is documented. Status: `not verified`. Fallback proposal: explicit polling design after API confirmation, with stale-state label and refresh timestamp.

## States and Recovery

| Area | Empty | Loading | Partial error | Permission denied | Timeout/offline | Retry |
| --- | --- | --- | --- | --- | --- | --- |
| Customer table | "No customers match these filters" | skeleton rows | keep filters and show table-level alert | explain role limitation | preserve current page and show retry | retry button |

## Security, Audit, and Export

- Escape cell content; do not render raw HTML.
- Neutralize CSV formulas before export.
- Export only fields allowed by role and PII policy.
- Audit create/update/delete/export with actor, action, entity, timestamp and correlation ID.

## Accessibility, Responsive, and Performance

- Use semantic table headers and `aria-sort`.
- Ensure keyboard access for filters, sort, row actions, modals and bulk actions.
- At 320px, prioritize key customer columns and move filters to a drawer.
- For 10k rows, use server-side pagination; do not load all rows client-side.

## Risks and Not Verified

- Backend authorization is not verified until middleware/policies/endpoints are inspected.
- KPI formulas and timezone are missing.
- Realtime cannot be claimed without channel evidence.
- No files were edited because the request was spec-only.
