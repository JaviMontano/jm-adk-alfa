<!--
generated-by: scripts/scaffold-skill.py
generated-for: google-sheets-mcp
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Example Input

Use `google-sheets-mcp` to plan a weekly KPI workbook workflow. [CODE]

## Request

Create a new Google Sheets workbook from a reviewed template, add a Raw tab,
write KPI headers, append the current week's metrics, and batch update a summary
range. [CODE]

## Constraints

- Compile the plan offline before live MCP execution. [CODE]
- Start with `spreadsheets.get` against the template metadata. [DOC]
- Use `drive.file` for the create/write plan if the created workbook stays inside app-created/opened file access. [DOC]
- Require `CONFIRM_SHEETS_MUTATION sheets-plan-001` before any create/update/append/batchUpdate call. [CODE]
- Do not claim scopes can be limited to the Raw or Summary sheet only. [DOC]
