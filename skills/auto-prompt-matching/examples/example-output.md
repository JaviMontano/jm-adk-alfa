# Example Output

## Routing Decision

- [CÓDIGO] Decision: `route`.
- [CÓDIGO] Selected skill: `xlsx-template-creator`.
- [INFERENCIA] Confidence band: `route`, because the request explicitly asks for deterministic XLSX workbook generation with formulas, validations, summary sheet, and fixtures.
- [CONFIG] Next action: activate `xlsx-template-creator`; do not execute it inside this routing packet.

## Candidate Scores

| Candidate | Source | Trigger Evidence | Purpose Evidence | Scope Fit | Penalties | Score | Decision |
|---|---|---:|---:|---:|---|---:|---|
| `xlsx-template-creator` | [CÓDIGO] `skills/xlsx-template-creator/SKILL.md` | 30 | 35 | 25 | 0 | 90 | selected |
| `brand-xlsx` | [CÓDIGO] `skills/brand-xlsx/SKILL.md` | 10 | 20 | 15 | branded-scope | 45 | rejected |
| `data-export` | [CÓDIGO] `skills/data-export/SKILL.md` | 5 | 15 | 10 | export-not-generation | 30 | rejected |

## Tie-Breaks

- [CONFIG] Explicit prefix: none.
- [CONFIG] Exact artifact type: XLSX narrows candidate set.
- [CONFIG] Narrower scope: `xlsx-template-creator` outranks broad export or branding skills.

## Validation

- [CÓDIGO] Selected route exists in inspected source.
- [CONFIG] `assets/routing-checklist.md` applied.
- [CONFIG] No downstream task executed.
- [CONFIG] Rejected alternatives and scope reasons are visible.
