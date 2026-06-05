# Example Input

Apply BMAD to a greenfield subscription analytics product.

Context:

- [EXPLICIT] Goal: help finance teams detect revenue leakage from billing exports.
- [EXPLICIT] Build type: SaaS dashboard.
- [EXPLICIT] User wants documentation-first workflow, not immediate code.
- [EXPLICIT] Use the full BMAD lifecycle unless Quick Flow criteria are met.
- [OPEN] Security and rollback constraints are not yet defined.

Expected behavior:

- Route Mary, John, Sally, Winston, Bob, Amelia, and Quinn by phase.
- Produce artifact chain from `project-context.md` through readiness gate.
- Block Phase 4 until readiness gate returns `PASS`.
