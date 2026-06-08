# Google Drive MCP Assets

These assets make the `google-drive-mcp` skill deterministic. They convert
Google Drive API and local MCP guidance into stable JSON/Markdown contracts used
by the offline compiler and examples.

## Files

- `manifest.json` lists every asset and its consumers.
- `google-drive-mcp-schema.json` defines the structured input contract.
- `query-policy.json` defines search/list query requirements.
- `scope-policy.json` defines least-privilege OAuth scope profiles.
- `upload-policy.json` defines Drive upload type selection.
- `sharing-permission-policy.json` defines permission roles and confirmation
  gates.
- `mime-export-map.json` defines Google Workspace export MIME mappings.
- `mcp-tool-contract.json` maps local Drive MCP tools to safe operation classes.
- `source-map.md` records the primary source set used by this skill.
- `google-drive-mcp-template.md` renders the deterministic Markdown report.

The assets are offline policy snapshots. They do not authenticate, query Drive,
or invoke MCP tools.
