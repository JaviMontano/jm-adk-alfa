# Skill Review: google-docs-mcp

## Verdict

- [CODE] Status: `dod-complete`.
- [CODE] Scope: one skill only, `skills/google-docs-mcp`.
- [CODE] Review date: 2026-06-01.

## DoD Evidence

- [CODE] `assets/manifest.json` lists every local asset and validates asset consumers.
- [CODE] `assets/google-docs-mcp-schema.json` defines the structured Docs MCP input contract.
- [CODE] `assets/docs-operation-policy.json` maps real Docs API methods: `documents.create`, `documents.get`, and `documents.batchUpdate`.
- [CODE] `assets/scope-policy.json` defines `documents.readonly`, `drive.file`, and escalation-only `documents` scope profiles.
- [CODE] `assets/mutation-confirmation-policy.json` defines the human-confirmation gate for mutating Docs operations.
- [CODE] `assets/mcp-tool-contract.json` classifies local `workspace-mcp` Docs tools as read-only or mutating.
- [CODE] `scripts/compile-google-docs-mcp.py` compiles structured JSON into Markdown without network, OAuth, Docs API, or MCP calls.
- [CODE] `scripts/check.sh` validates a positive fixture plus missing confirmation, invalid create-body, and batch-without-get fixtures.
- [CODE] `evals/evals.json` contains concrete Docs MCP cases with `assets`, `deterministic_scripts`, and `quality_criteria` checks.
- [CODE] `templates/output.md` and `templates/output.html` define stable Markdown and HTML output shapes.
- [CODE] `examples/example-input.md` and `examples/example-output.md` are Docs-specific and no longer scaffold placeholders.

## Source Evidence

- [DOC] Local MCP setup: `docs/google-workspace-mcp-setup.md` documents `workspace-mcp`, Google Workspace tools, read-only mode, and service-level permissions.
- [DOC] Local MCP integration: `docs/mcp-integration.md` documents project `.mcp.json`, `workspace-mcp`, and secret-handling guidance.
- [DOC] Google Docs API REST reference: https://developers.google.com/workspace/docs/api/reference/rest
- [DOC] Google Docs scopes: https://developers.google.com/workspace/docs/api/auth
- [DOC] Google Docs `documents.batchUpdate`: https://developers.google.com/workspace/docs/api/reference/rest/v1/documents/batchUpdate
- [DOC] Google Docs `documents.create`: https://developers.google.com/workspace/docs/api/reference/rest/v1/documents/create
- [DOC] Google Docs `documents.get`: https://developers.google.com/workspace/docs/api/reference/rest/v1/documents/get
- [DOC] Google Workspace MCP developer server: https://developers.google.com/workspace/guides/build-with-llms
- [DOC] MCP tools spec: https://modelcontextprotocol.io/specification/draft/server/tools

## Validation Commands

```bash
python3 -B scripts/validate-skill-dod.py --skill google-docs-mcp
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill google-docs-mcp
bash skills/google-docs-mcp/scripts/check.sh
python3 -B -m py_compile skills/google-docs-mcp/scripts/*.py
git diff --check
```

## Residual Limits

- [INFERENCE] This review certifies the `google-docs-mcp` skill only.
- [INFERENCE] The deterministic script validates a plan/checklist contract; it does not prove live Google Docs access, document existence, OAuth scope grant, or MCP server availability.
- [INFERENCE] Live mutations remain dependent on user confirmation, current document ACLs, revision state, Workspace admin policy, and valid document indexes.
