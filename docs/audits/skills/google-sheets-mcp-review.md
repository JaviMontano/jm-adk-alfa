# Skill Review: google-sheets-mcp

## Verdict

- [CODE] Status: `dod-complete`.
- [CODE] Scope: one skill only, `skills/google-sheets-mcp`.
- [CODE] Review file: `docs/audits/skills/google-sheets-mcp-review.md`.
- [CODE] Review date: 2026-06-01.

## DoD Evidence

- [CODE] `assets/manifest.json` lists every local asset and validates asset consumers.
- [CODE] `assets/google-sheets-mcp-schema.json` defines the structured Sheets MCP input contract.
- [CODE] `assets/scope-policy.json` defines `spreadsheets.readonly`, `drive.file`, `spreadsheets`, and broad `drive` profiles.
- [DOC] `assets/scope-policy.json` includes the official note that Sheets API scopes apply to a spreadsheet file and cannot be limited to a specific sheet.
- [CODE] `assets/mcp-tool-contract.json` maps local `workspace-mcp` tool names to official Sheets REST methods.
- [CODE] `assets/operation-safety-policy.json` defines read-only-first and human-confirmation gates.
- [CODE] `assets/value-range-policy.json` defines ValueRange requirements, value input options, append behavior, and render defaults.
- [CODE] `assets/batch-update-policy.json` defines structural `spreadsheets.batchUpdate` rules and atomicity guidance.
- [CODE] `scripts/compile-google-sheets-mcp.py` compiles structured JSON into Markdown without network, OAuth, Google Sheets, or MCP calls.
- [CODE] `scripts/check.sh` validates a positive fixture plus missing confirmation, missing read-only-first, and invalid sheet-level scope fixtures.
- [CODE] `evals/evals.json` contains concrete Sheets MCP cases with `assets`, `deterministic_scripts`, and `quality_criteria` checks.
- [CODE] `examples/example-input.md` and `examples/example-output.md` are Sheets-specific and no longer scaffold placeholders.
- [CODE] `templates/output.md` and `templates/output.html` expose summary, evidence, MCP preflight, scope note, operation plan, value contract, batchUpdate contract, confirmation gate, validation, and risks.

## Source Evidence

- [DOC] Local MCP setup: `docs/google-workspace-mcp-setup.md` documents `workspace-mcp`, Sheets service activation, read-only mode, and service-level permissions.
- [DOC] Local MCP integration: `docs/mcp-integration.md` documents project `.mcp.json`, `workspace-mcp`, and MCP skill usage.
- [DOC] Google Sheets API REST overview: https://developers.google.com/workspace/sheets/api/reference/rest
- [DOC] Google Sheets scopes: https://developers.google.com/workspace/sheets/api/scopes
- [DOC] Google Sheets `spreadsheets.create`: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/create
- [DOC] Google Sheets `spreadsheets.get`: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/get
- [DOC] Google Sheets `spreadsheets.batchUpdate`: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/batchUpdate
- [DOC] Google Sheets `spreadsheets.values`: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets.values
- [DOC] Google Workspace MCP developer server: https://developers.google.com/workspace/guides/build-with-llms
- [DOC] MCP tools spec: https://modelcontextprotocol.io/specification/draft/server/tools

## Validation Commands

```bash
python3 -B scripts/validate-skill-dod.py --skill google-sheets-mcp
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill google-sheets-mcp
bash skills/google-sheets-mcp/scripts/check.sh
python3 -B -m py_compile skills/google-sheets-mcp/scripts/*.py
git diff --check
```

## Residual Limits

- [INFERENCE] This review certifies the `google-sheets-mcp` skill only.
- [INFERENCE] The deterministic script validates a plan/checklist contract; it does not prove live spreadsheet existence, OAuth grant, user permissions, formulas, protected ranges, collaborator state, or MCP server availability.
- [INFERENCE] Live mutation remains dependent on human confirmation, target spreadsheet permissions, Workspace admin policy, range correctness, and current spreadsheet state.
