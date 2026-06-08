# Example Output

## Summary

- [CODE] `gdocs-p007-runbook-dod` compiles a safe Google Docs MCP checklist.
- [CODE] Planned Docs API methods: `documents.create`, `documents.get`, and
  `documents.batchUpdate`.
- [CODE] The compiler mode is offline only.

## Evidence

- [DOC] Local setup: `docs/google-workspace-mcp-setup.md`.
- [DOC] Local MCP integration: `docs/mcp-integration.md`.
- [DOC] Official Docs API source map: `assets/source-map.md`.

## Scope Review

| Operation | Scope Profile | Rationale |
|---|---|---|
| Inspect document | `docs_readonly` | Read-only structure inspection |
| Create or update app-created document | `drive_file` | Preferred mutation scope for app-created or user-opened files |

## Docs API Plan

| ID | Docs API Method | Safety Gate |
|---|---|---|
| `create-runbook-doc` | `documents.create` | Title-only create payload and human confirmation |
| `inspect-runbook-doc` | `documents.get` | Structure and revision captured before edit |
| `insert-runbook-sections` | `documents.batchUpdate` | Ordered requests, write control, and human confirmation |

## Validation

- [CODE] `documents.create` does not include body content.
- [CODE] `documents.batchUpdate` has a prior `documents.get` for the same document.
- [CODE] Mutating operations are blocked until confirmation text is retained.
- [CODE] No Docs, OAuth, network, or MCP calls are performed by the compiler.

## Risks and Limits

- [INFERENCE] Live execution can still fail if the document ACL, OAuth grant,
  revision ID, or document indexes differ at execution time.
- [ASSUMPTION] Document IDs and revision IDs come from a trusted read-only
  discovery step.
