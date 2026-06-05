# BMAD Plan

[EXPLICIT] Start a greenfield SaaS product with the full BMAD lifecycle.

# Lifecycle Routing

- [EXPLICIT] Phase 1 Mary creates `product-brief.md`.
- [EXPLICIT] Phase 2 John creates `PRD.md`; Sally creates `ux-spec.md`.
- [EXPLICIT] Phase 3 Winston creates `architecture.md`; Bob creates `stories/*.md`.
- [EXPLICIT] Phase 4 waits for readiness gate PASS.

# Persona Routing

| Need | Persona | Reason |
|---|---|---|
| Problem discovery | Mary | [EXPLICIT] Phase 1 owner |
| PRD | John | [EXPLICIT] Planning owner |
| Architecture | Winston | [EXPLICIT] Solutioning owner |

# Artifact Chain

`project-context.md` -> `product-brief.md` -> `PRD.md` -> `architecture.md` -> `stories/*.md` -> `readiness-gate.md`

# Readiness Gate

- **Result:** [OPEN] Not run yet.
- **Phase 4:** [EXPLICIT] Not allowed until PASS.

# Validation

- [EXPLICIT] Code starts only after the readiness gate returns PASS.
- [EXPLICIT] All artifacts are source-backed.

# Risks and Open Questions

- [OPEN] Market assumptions require user-supplied evidence.
