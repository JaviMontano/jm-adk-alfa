<!--
generated-by: scripts/scaffold-skill.py
generated-for: knowledge-management
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

The checkout modernization knowledge base has one contradiction, one stale
runbook, and one unowned action that blocks handoff readiness. [DOC][INFERENCIA]

## Knowledge Register

| id | type | source | owner | status | retrieval_terms | next_action |
|----|------|--------|-------|--------|-----------------|-------------|
| km-001 | decision | `docs/decisions/checkout-auth.md` | Identity Team | active | checkout auth, SSO, enterprise buyers | Keep as canonical auth policy. |
| km-002 | runbook | `docs/runbooks/checkout-retry.md` | Platform Ops | stale | retry queue, payment failure, checkout retry | Review retry queue runbook by 2026-06-14. |
| km-003 | note | `docs/notes/session-44.md` | Unassigned | contradiction | guest checkout, enterprise buyers | Resolve guest checkout vs SSO policy. |
| km-004 | task | `docs/tasklog.md` | Payments Team | gap | payment taxonomy, failure categories | Assign launch owner and acceptance evidence. |

## Searchability Map

- `checkout auth` -> `docs/decisions/checkout-auth.md` [DOC]
- `retry queue` -> `docs/runbooks/checkout-retry.md` [DOC]
- `guest checkout` -> `docs/notes/session-44.md` [DOC]
- `payment taxonomy` -> `docs/tasklog.md` [DOC]

## Decay Review

- Reference date: 2026-06-06. [CONFIG]
- `km-002` is stale because the runbook was last reviewed on 2026-02-01 and
  exceeds the 90-day runbook freshness window. [DOC][INFERENCIA]

## Gaps And Contradictions

- `km-003` conflicts with `km-001`: guest checkout allowed vs SSO mandatory for
  enterprise buyers. [DOC][INFERENCIA]
- `km-004` lacks an explicit launch owner and acceptance evidence. [DOC]

## Action Log

| action | owner | due_date | evidence |
|--------|-------|----------|----------|
| Resolve enterprise checkout auth policy conflict | Identity Team | 2026-06-10 | `docs/decisions/checkout-auth.md`, `docs/notes/session-44.md` |
| Refresh retry queue runbook | Platform Ops | 2026-06-14 | `docs/runbooks/checkout-retry.md` |
| Assign payment taxonomy owner | Payments Team | 2026-06-08 | `docs/tasklog.md` |

## Validation

- All register items include a source path, owner or escalation target,
  evidence tag, retrieval terms, and next action. [DOC]
- Decay status uses explicit reference date `2026-06-06`, not the live clock.
  [CONFIG]
- Remaining risk: if `docs/notes/session-44.md` is unofficial, the conflict may
  be downgraded after source-priority review. [SUPUESTO]
