# Google Sheets MCP Assets

These assets make `google-sheets-mcp` deterministic by converting official
Google Sheets REST guidance, MCP tool-contract guidance, and local Workspace MCP
setup docs into stable offline policies. [CODE]

## Files

- `manifest.json` lists every asset and its consumers. [CODE]
- `google-sheets-mcp-schema.json` defines the structured input contract. [CODE]
- `scope-policy.json` defines least-privilege OAuth scope profiles and the official spreadsheet-file scope note. [DOC]
- `mcp-tool-contract.json` maps local Workspace MCP tools to Sheets REST methods. [CODE]
- `operation-safety-policy.json` defines read-only-first and human-confirmation gates. [CODE]
- `value-range-policy.json` defines value operation defaults and `ValueRange` requirements. [DOC]
- `batch-update-policy.json` defines structural `spreadsheets.batchUpdate` request rules. [DOC]
- `source-map.md` records the primary official and local source set. [DOC]
- `google-sheets-mcp-template.md` renders the deterministic Markdown report. [CODE]

The assets are offline snapshots. They do not authenticate, query Sheets, or
invoke MCP tools. [CODE]
