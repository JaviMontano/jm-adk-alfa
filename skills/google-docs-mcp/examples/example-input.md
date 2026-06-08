# Example Input

Plan a Google Docs MCP workflow for a runbook document.

Requirements:

- Create a blank Google Doc titled `P-007 Runbook DoD Checklist`.
- Inspect the created document before editing.
- Insert a heading and checklist items with `documents.batchUpdate`.
- Use the minimum practical scope profile.
- Do not call live Google Docs, OAuth, network, or MCP tools during planning.
- Require explicit human confirmation before any live mutation.

Accepted operation shape:

- `documents.create` for title-only document creation.
- `documents.get` for document structure, tabs, and revision ID.
- `documents.batchUpdate` for ordered insert/style/bullet requests.
