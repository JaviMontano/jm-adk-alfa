# Example Output

## Summary

Scope: Payment onboarding modernization

| Metric | Value |
|---|---:|
| Total assumptions | 4 |
| Open assumptions | 2 |
| Validated | 1 |
| Invalidated | 1 |
| High-impact open | 1 |
| Assumption ratio | 50% |
| Overall risk | high |

## Assumptions

| ID | Statement | Status | Evidence Tag | Evidence | Impact | Validation Action | Owner | Decision Link |
|---|---|---|---|---|---|---|---|---|
| A-001 | Enterprise customers can complete onboarding without assisted data migration. | unvalidated | [ASSUMPTION] | Stakeholder workshop stated this as a target outcome but provided no usage data. | high | Review last 20 enterprise onboarding tickets and migration requests. | Product | DL-014 |
| A-002 | The current service exposes onboarding events needed by the new dashboard. | validated | [CODE] | `services/events/onboarding.py` defines `account_created` and `data_import_completed`. | medium | No action required until event contract changes. | Engineering | ADR-003 |
| A-003 | The program must use Firebase as the only persistence layer. | invalidated | [DOC] | ADR-003 approves Supabase for operational analytics. | critical | Update planning docs to remove Firebase-only constraint. | Architecture | ADR-003 |
| A-004 | Marketing can supply localized onboarding copy before launch freeze. | blocked | [ASSUMPTION] | Launch plan names Marketing as owner but has no due date. | low | Request copy freeze date from Marketing lead. | Marketing | DL-015 |

## Contradictions

| ID | Assumptions | Description | Resolution Action |
|---|---|---|---|
| C-001 | A-003 | Firebase-only persistence conflicts with ADR-003 Supabase analytics approval. | Treat A-003 as invalidated and update architecture assumptions. |

## Decision Links

| Decision | Assumptions | Status |
|---|---|---|
| DL-014 | A-001 | open |
| ADR-003 | A-002, A-003 | accepted |

## Validation Queue

| Assumption | Action | Owner | Due Basis |
|---|---|---|---|
| A-001 | Review onboarding tickets and quantify migration demand. | Product | Before scope freeze |
| A-004 | Request localized copy freeze date. | Marketing | Before launch readiness review |

## Warnings

- `HIGH_ASSUMPTION_RATIO`: 50% of entries use `[ASSUMPTION]`; do not ship
  implementation scope until high-impact open assumptions are validated.
