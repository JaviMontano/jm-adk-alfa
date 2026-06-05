# BMAD Plan

[EXPLICIT] Use Barry Quick Flow for a one-file typo fix.

# Lifecycle Routing

- [EXPLICIT] Quick Flow bypasses PRD and architecture because the change is <=3 story points with no architecture, security, or data-contract impact.

# Persona Routing

| Need | Persona | Reason |
|---|---|---|
| triage | Barry | [EXPLICIT] Quick Flow owner |
| rapid spec | Barry | [EXPLICIT] Small change owner |
| test or self-review | Barry | [EXPLICIT] Verification owner |

# Artifact Chain

`quick-triage.md` -> `rapid-spec.md` -> `change.md` -> `test or self-review`

# Readiness Gate

- **Result:** [EXPLICIT] Quick Flow eligible.
- **Phase 4:** [EXPLICIT] Scoped to the approved small change only.

# Validation

- [EXPLICIT] Barry handles triage, rapid spec, change, and test or self-review.

# Risks and Open Questions

- [OPEN] Escalate to full BMAD if the fix reveals architecture impact.
