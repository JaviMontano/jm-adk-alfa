# Google Slides MCP Assets

These assets are loaded by `scripts/compile-google-slides-mcp.py` to produce an offline operation plan. They encode stable Google Slides REST operations, MCP tool mapping, least-privilege scope profiles, human-confirmation policy, and the Markdown report template.

## Files

| File | Purpose |
|---|---|
| `google-slides-mcp-schema.json` | Stable structured input contract for offline plans. |
| `mcp-tool-contract.json` | Maps `workspace-mcp` tools to real Slides REST methods. |
| `scope-policy.json` | Defines minimum OAuth scope profiles and broad-scope exceptions. |
| `human-confirmation-policy.json` | Defines mutation confirmation status, phrase, and required fields. |
| `slides-batchupdate-request-policy.json` | Lists supported `batchUpdate` request keys and write-control guidance. |
| `thumbnail-policy.json` | Defines thumbnail size, MIME type, and `contentUrl` handling rules. |
| `google-slides-operation-template.md` | Canonical deterministic Markdown report template. |
| `source-map.md` | Primary and local source map used to maintain the skill. |
