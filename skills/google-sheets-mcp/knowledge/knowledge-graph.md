# Google Sheets MCP Knowledge Graph

- [CODE] `google-sheets-mcp` loads local assets and fixtures through `scripts/compile-google-sheets-mcp.py`.
- [DOC] The official REST surface includes `spreadsheets.create`, `spreadsheets.get`, `spreadsheets.batchUpdate`, and `spreadsheets.values.*`.
- [DOC] Sheets OAuth scopes bind to the spreadsheet file rather than a single sheet/tab.
- [CODE] Human confirmation gates every mutating operation in the deterministic compiler.
- [INFERENCE] `google-drive-mcp` should handle file search/sharing tasks before Sheets-specific value or structure operations begin.
