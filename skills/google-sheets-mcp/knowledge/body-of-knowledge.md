<!--
generated-by: scripts/scaffold-skill.py
generated-for: google-sheets-mcp
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Google Sheets MCP Body of Knowledge

## Canonical REST Surface

- `spreadsheets.create` creates a spreadsheet and returns the new spreadsheet resource. [DOC]
- `spreadsheets.get` returns spreadsheet metadata and can limit grid data with ranges and field masks. [DOC]
- `spreadsheets.batchUpdate` applies structural spreadsheet updates and validates all requests before applying any request. [DOC]
- `spreadsheets.values.get` reads a range of values by spreadsheet ID and A1/R1C1 range. [DOC]
- `spreadsheets.values.update` sets values in one range and requires `valueInputOption`. [DOC]
- `spreadsheets.values.append` appends values after a detected table in a range and requires `valueInputOption`. [DOC]
- `spreadsheets.values.batchUpdate` writes one or more `ValueRange` objects and requires `valueInputOption`. [DOC]

## Scope Policy

- `https://www.googleapis.com/auth/spreadsheets.readonly` is the read-only Sheets scope profile. [DOC]
- `https://www.googleapis.com/auth/drive.file` is the preferred per-file mutation scope when app-created/app-opened files are enough. [DOC]
- `https://www.googleapis.com/auth/spreadsheets` grants edit/create/delete access to all accessible Google Sheets spreadsheets and is broader than `drive.file`. [DOC]
- `https://www.googleapis.com/auth/drive` is restricted and should not be the default for Sheets-only plans. [DOC]
- Official Sheets API scopes apply to a spreadsheet file and cannot be limited to a specific sheet. [DOC]

## MCP Contract

- Local docs identify `workspace-mcp` as the unified Google Workspace MCP server. [DOC]
- The skill maps local tool names to official Sheets REST operations in `assets/mcp-tool-contract.json`. [CODE]
- MCP tool definitions require a unique tool name, description, and JSON `inputSchema`; structured results should conform to any declared `outputSchema`. [DOC]
- The deterministic compiler emits a plan/checklist and does not call live MCP tools. [CODE]

## Safety Heuristics

- Start mixed or mutating workflows with `spreadsheets.get` or `spreadsheets.values.get`. [CODE]
- Keep `includeGridData=false` unless grid data is required. [INFERENCE]
- Prefer `spreadsheets.values.batchUpdate` for multiple value ranges. [INFERENCE]
- Use `spreadsheets.batchUpdate` for structural changes such as sheet creation, protected ranges, formatting, dimensions, validation, and named ranges. [DOC]
- Treat formulas, protected ranges, and concurrent collaborators as residual risks that need human review. [INFERENCE]
