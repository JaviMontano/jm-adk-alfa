# Gmail MCP Assets

Deterministic resources for the `gmail-mcp` skill.

- `gmail-mcp-schema.json` defines the structured offline input accepted by `scripts/compile-gmail-mcp.py`.
- `operation-safety-policy.json` defines read-only-first ordering, confirmation gates, and forbidden automation.
- `scope-matrix.json` maps Gmail operations to the minimum scope family to verify before calling MCP tools.
- `search-query-patterns.json` captures safe Gmail search patterns, `q` usage, `labelIds[]`, and date caveats.
- `label-policy.json` captures system/user label constraints and bulk label confirmation rules.
- `send-draft-policy.json` captures draft-first sending, send confirmations, and recipient review requirements.
- `privacy-redaction-policy.json` defines what must never be logged, stored, or returned unredacted.
- `gmail-mcp-template.md` is the deterministic Markdown report template used by the compiler.
