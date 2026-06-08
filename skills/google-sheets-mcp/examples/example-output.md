<!--
generated-by: scripts/scaffold-skill.py
generated-for: google-sheets-mcp
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

- [CODE] Request `sheets-plan-001` compiles an offline Google Sheets MCP plan for a weekly KPI workbook.
- [CODE] The plan starts with `spreadsheets.get`, then gates `spreadsheets.create`, `spreadsheets.batchUpdate`, `spreadsheets.values.update`, `spreadsheets.values.append`, and `spreadsheets.values.batchUpdate` behind human confirmation.

## Scope Review

- [DOC] Read-only discovery can use `https://www.googleapis.com/auth/spreadsheets.readonly`.
- [DOC] App-created/opened mutations can use `https://www.googleapis.com/auth/drive.file`.
- [DOC] Sheets scopes apply to the spreadsheet file and cannot be limited to a specific sheet/tab.

## Operation Plan

| Step | REST method | MCP tool | Gate |
|---|---|---|---|
| 1 | `spreadsheets.get` | `mcp__workspace-mcp__get_spreadsheet_info` | read-only-first |
| 2 | `spreadsheets.create` | `mcp__workspace-mcp__create_spreadsheet` | human confirmation |
| 3 | `spreadsheets.batchUpdate` | `mcp__workspace-mcp__format_sheet_range` | human confirmation |
| 4 | `spreadsheets.values.get` | `mcp__workspace-mcp__read_sheet_values` | read-only check |
| 5 | `spreadsheets.values.update` | `mcp__workspace-mcp__modify_sheet_values` | human confirmation |
| 6 | `spreadsheets.values.append` | `mcp__workspace-mcp__modify_sheet_values` | human confirmation |
| 7 | `spreadsheets.values.batchUpdate` | `mcp__workspace-mcp__modify_sheet_values` | human confirmation |

## Validation

- [CODE] `bash skills/google-sheets-mcp/scripts/check.sh` validates the deterministic compiler and fixtures.
- [CODE] Invalid fixtures reject missing confirmation, missing read-only-first discovery, and sheet/tab-level scope binding.

## Risks

- [INFERENCE] The offline compiler cannot verify live permissions, formulas, protected ranges, or collaborator state.
