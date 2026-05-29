# Example Input

Design an implementation-ready admin dashboard spec for an internal CRM.

Context:

- Entities: customers, orders, support tickets.
- Roles: viewer, editor, admin.
- Existing backend: REST endpoints are documented for customers only; orders and tickets APIs are not confirmed.
- Tables: customer list with 10k records, filters by status/owner/date, search by email, CSV export, and bulk owner reassignment.
- CRUD: create/edit customer; delete customer is irreversible and requires admin role.
- Metrics: active customers, overdue tickets, monthly order volume. Formulas and timezone are not documented.
- Realtime: requested for ticket updates, but no channel is documented.
- Requirements: responsive at 320px/tablet/desktop, keyboard accessible, audit all create/update/delete/export actions, no file edits yet.
