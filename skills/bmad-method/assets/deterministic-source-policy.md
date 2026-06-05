# Deterministic Source Policy

- Use repository files and user-supplied sources first.
- Do not use network research by default.
- If external research is explicitly requested, record the source URL and retrieval date supplied by the user or command context.
- Replace non-deterministic review with stable-order sampling: first 10 claims after document-order extraction.
- Do not fabricate BMAD scripts, templates, personas, or artifact paths. If a referenced runtime asset is absent, present it as a required artifact to create, not as an executable command.
- Phase 4 implementation requires readiness gate `PASS`.
