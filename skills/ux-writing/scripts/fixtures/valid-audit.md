# UX Writing Audit

## Audience And Source

- [CONFIG] Audience: finance analysts using a billing dashboard.
- [DOC] Source action: analysts review invoices and export CSV files.
- [SUPUESTO] Product capabilities beyond CSV export are not provided.

## Findings

| Finding | Evidence | UX Writing Risk |
|---|---|---|
| Generic button | [DOC] "Submit" | Action is unclear. |
| Generic link | [DOC] "Click here" | Destination is hidden. |
| Dead empty state | [DOC] "No data available" | No next action. |

## Rewrites

| ID | Type | Before | After | Why |
|---|---|---|---|---|
| RW-1 | CTA | Submit | Review Invoice | Verb + Object names the action. |
| RW-2 | Link | Click here | View Export Options | Link text describes destination. |
| RW-3 | Help text | More info | Learn which invoice fields export to CSV. | Uses known CSV fact. |
| RW-4 | Error | Invalid amount | Amount must be within the allowed billing range. Check the value and try again. | States issue and fix. |
| RW-5 | Empty state | No data available | No invoices selected yet. Select invoices to prepare a CSV export. | States missing item and next action. |

## Accessibility And Readability

- [INFERENCIA] Labels stand alone without relying on position or color.
- [CONFIG] Reading-level target is business-readable dashboard copy.

## Validation

- [CONFIG] Five before/after rewrites are present.
- [CONFIG] Unsupported product claims are not included.
