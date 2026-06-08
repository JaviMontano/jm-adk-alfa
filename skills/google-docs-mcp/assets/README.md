# Google Docs MCP Assets

These assets define the deterministic, offline contract for `google-docs-mcp`.
They are consumed by `scripts/compile-google-docs-mcp.py` and by the skill docs.

## Files

- `manifest.json` lists every local asset and its consumers.
- `google-docs-mcp-schema.json` defines the structured input contract.
- `docs-operation-policy.json` maps supported Docs API methods and request types.
- `scope-policy.json` defines least-privilege OAuth scope profiles.
- `mutation-confirmation-policy.json` defines human-confirmation gates.
- `mcp-tool-contract.json` maps local `workspace-mcp` Docs tools.
- `source-map.md` records primary local and official sources.
- `google-docs-mcp-template.md` renders the offline Markdown report.
