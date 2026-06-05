# UX Writing Audit

## Audience And Source

- [CONFIG] Audience: finance analysts using a billing dashboard.
- [DOC] Source actions: review invoices and export CSV files.
- [SUPUESTO] Product capabilities beyond CSV export are not provided.

## Findings

| Finding | Evidence | UX Writing Risk |
|---|---|---|
| Generic button | [DOC] "Submit" | Action is unclear without context. |
| Generic link | [DOC] "Click here" | Link text does not describe destination. |
| Weak helper text | [DOC] "More info" | User cannot predict what help they will get. |
| Unhelpful error | [DOC] "Invalid amount" | Error omits what happened and how to fix. |
| Dead empty state | [DOC] "No data available" | Empty state omits what is missing and next action. |

## Rewrites

| ID | Type | Before | After | Why |
|---|---|---|---|---|
| RW-1 | CTA | Submit | Review Invoice | Verb + Object names the user action. |
| RW-2 | Link | Click here | View Export Options | Link text describes the destination. |
| RW-3 | Help text | More info | Learn which invoice fields export to CSV. | Defines the help topic using known facts. |
| RW-4 | Error | Invalid amount | Amount must be within the allowed billing range. Check the value and try again. | States issue and fix without blame. |
| RW-5 | Empty state | No data available | No invoices selected yet. Select invoices to prepare a CSV export. | States what is missing and the next action. |

## Accessibility And Readability

- [INFERENCIA] Avoid color-only or location-only instructions; each action label should stand alone.
- [INFERENCIA] Sentences are short and written for a dashboard scan, not a long document.
- [CONFIG] Reading-level target: business-readable, short labels, no unexplained jargon.

## Validation

- [CONFIG] Five before/after rewrites are present.
- [CONFIG] Generic anti-patterns are replaced: Submit, Click here, More info, Invalid amount, and No data available.
- [CONFIG] No unsupported claim is made about AI, SOC 2, real-time sync, or approval workflow.
