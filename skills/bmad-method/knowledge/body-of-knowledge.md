# BMAD Method — Body of Knowledge

## Canon

BMAD is a documentation-first lifecycle for AI-driven development. It routes work through artifacts and specialized personas before implementation.

## Deterministic Principles

| Principle | Rule |
|---|---|
| Artifact chain | Each phase consumes prior approved artifacts |
| Persona routing | Use `assets/persona-matrix.json` |
| Phase 4 gate | Implementation starts only after readiness `PASS` |
| Quick Flow | Barry applies only to small, low-risk changes |
| Source policy | Use local/user-supplied sources unless external research is explicit |

## Anti-Patterns

| Anti-Pattern | Corrective Action |
|---|---|
| Skip docs and code | Block Phase 4 and route to readiness gate |
| Invent scripts/templates | Mark required artifact as missing |
| Random checks | Use stable-order sampling |
| God agent | Route to persona owner |
