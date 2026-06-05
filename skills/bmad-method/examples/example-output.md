# Example Output

```markdown
# BMAD Plan

[EXPLICIT] Use full greenfield BMAD because this is a new SaaS dashboard and the user asked for documentation-first workflow.

# Lifecycle Routing

- [EXPLICIT] Phase 1: Mary creates `product-brief.md` with problem, audience, assumptions, and success metrics.
- [EXPLICIT] Phase 2: John creates `PRD.md`; Sally creates `ux-spec.md`.
- [EXPLICIT] Phase 3: Winston creates `architecture.md`; Bob creates `epics/*.md` and `stories/*.md`.
- [EXPLICIT] Phase 4: Amelia and Quinn begin only after readiness gate `PASS`.

# Persona Routing

| Phase | Persona | Artifact |
|---|---|---|
| 1 | Mary | `product-brief.md` |
| 2 | John | `PRD.md` |
| 2 | Sally | `ux-spec.md` |
| 3 | Winston | `architecture.md` |
| 3 | Bob | `stories/*.md` |

# Artifact Chain

`project-context.md` -> `product-brief.md` -> `PRD.md` -> `ux-spec.md` -> `architecture.md` -> `ADRs` -> `stories/*.md` -> `readiness-gate.md`

# Readiness Gate

- **Result:** [OPEN] Not run yet.
- **Phase 4:** [EXPLICIT] blocked until `PASS`.
- **Open blockers:** [OPEN] security and rollback constraints.

# Validation

- [EXPLICIT] No immediate code is produced.
- [EXPLICIT] Gate vocabulary uses PASS/CONCERNS/FAIL only.
- [EXPLICIT] Stable-order sampling applies to claim review.

# Risks and Open Questions

- [OPEN] Billing export formats are not supplied.
- [OPEN] Security constraints need a human owner before Phase 4.
```
