<!--
generated-by: scripts/scaffold-skill.py
generated-for: google-sheets-mcp
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Google Sheets MCP Meta Prompt

Review whether `google-sheets-mcp` should activate, whether the request is safe,
and which support agents should participate. [CODE]

## Activation Check

- Activate for Google Sheets, spreadsheet cell values, A1 ranges, Sheets MCP, or official Sheets REST methods. [CODE]
- Prefer `google-drive-mcp` when the dominant task is file search, sharing, upload, or export rather than spreadsheet values/structure. [INFERENCE]
- Ask for missing spreadsheet ID/range/confirmation before live mutation. [CODE]
- Do not activate for unrelated tabular analysis without a Sheets or MCP intent. [CODE]

## Safety Routing

- Lead owns the plan and offline compiler. [CODE]
- Specialist reviews ValueRange, batchUpdate, and scope details. [CODE]
- Guardian blocks unconfirmed mutations or sheet/tab-level scope assumptions. [CODE]
- Support checks fixtures, examples, and deterministic script output. [CODE]
