<!--
generated-by: scripts/scaffold-skill.py
generated-for: google-sheets-mcp
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Google Sheets MCP Primary Prompt

## Objective

Produce a deterministic Google Sheets MCP plan/checklist that maps the user's
goal to official Sheets REST methods, minimum OAuth scopes, and explicit
mutation gates. [DOC]

## Required Inputs

- Goal
- Spreadsheet identifier or create-new intent. [CODE]
- Target sheet names and A1 ranges for value operations. [CODE]
- Read-only or mutating operation intent. [CODE]
- Scope constraints and confirmation status. [CODE]
- Definition of done and validation commands. [CODE]

## Process

1. Classify the requested operation as read-only or mutating. [CODE]
2. Select the REST method family: `spreadsheets.*` or `spreadsheets.values.*`. [DOC]
3. Apply the minimum scope profile from `assets/scope-policy.json`. [CODE]
4. For mutations, require read-only-first discovery and human confirmation. [CODE]
5. Compile the offline plan with `scripts/compile-google-sheets-mcp.py` when structured input is available. [CODE]
6. Validate with `scripts/check.sh` before marking the skill DoD complete. [CODE]

## Output

Return Markdown or HTML with summary, evidence, MCP preflight, official scope
note, operation table, value contract, structural batch update contract,
confirmation gate, validation, and residual risks. [CODE]
