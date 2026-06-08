<!--
generated-by: scripts/scaffold-skill.py
generated-for: google-sheets-mcp
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Google Sheets MCP

Deterministic Google Sheets MCP planning skill for safe spreadsheet reads,
value writes, structural batch updates, and new spreadsheet creation. [CODE]

## Triggers

- google-sheets-mcp
- spreadsheet
- google sheets
- sheet data
- values.get
- values.update
- values.append
- values.batchUpdate
- spreadsheets.batchUpdate

## Allowed Tools

- Read
- Write
- Bash
- mcp__workspace-mcp__read_sheet_values
- mcp__workspace-mcp__modify_sheet_values
- mcp__workspace-mcp__create_spreadsheet
- mcp__workspace-mcp__list_spreadsheets
- mcp__workspace-mcp__get_spreadsheet_info
- mcp__workspace-mcp__format_sheet_range

## Quick Use

Use this skill when the request needs a Sheets MCP plan/checklist grounded in
official Sheets REST methods and local Workspace MCP setup docs. [DOC]

```bash
python3 skills/google-sheets-mcp/scripts/compile-google-sheets-mcp.py \
  --input skills/google-sheets-mcp/scripts/fixtures/google-sheets-mcp-input.json

bash skills/google-sheets-mcp/scripts/check.sh
```

## Deterministic Contract

- The compiler reads local `assets/` and JSON fixtures only. [CODE]
- The compiler never calls Google Sheets, OAuth, HTTP, or MCP tools. [CODE]
- Mutating operations require human confirmation. [CODE]
- Mutating workflows must start with a read-only `spreadsheets.get` or `spreadsheets.values.get` operation. [CODE]
- Sheets scopes bind to the spreadsheet file, not to a specific sheet/tab. [DOC]

## Output Format

Markdown or HTML plan with summary, evidence, MCP preflight, scope review,
operation plan, value contract, structural batch update contract, confirmation
gate, validation, and risks. [CODE]
