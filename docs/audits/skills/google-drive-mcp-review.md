# Skill Review: google-drive-mcp

## Verdict

- [CODE] Status: `dod-complete`.
- [CODE] Scope: one skill only, `skills/google-drive-mcp`.
- [CODE] Review date: 2026-06-01.

## DoD Evidence

- [CODE] `assets/manifest.json` lists every local asset and validates asset consumers.
- [CODE] `assets/google-drive-mcp-schema.json` defines the structured Drive MCP input contract.
- [CODE] `assets/query-policy.json` defines `q`, `fields`, `trashed = false`, `spaces`, `corpora`, and pagination defaults.
- [CODE] `assets/scope-policy.json` defines `drive.file`, `drive.readonly`, `drive.metadata.readonly`, and full `drive` scope profiles.
- [CODE] `assets/upload-policy.json` defines `uploadType=media`, `multipart`, and `resumable` selection.
- [CODE] `assets/sharing-permission-policy.json` defines permission types, roles, `canShare`, and human confirmation gates.
- [CODE] `assets/mime-export-map.json` defines Google Workspace export MIME mappings.
- [CODE] `assets/mcp-tool-contract.json` classifies local `workspace-mcp` Drive tools as read-only or mutating.
- [CODE] `scripts/compile-google-drive-mcp.py` compiles structured JSON into Markdown without network, OAuth, Drive, or MCP calls.
- [CODE] `scripts/check.sh` validates a positive fixture, expected output fragments, missing `trashed = false`, and missing sharing confirmation.
- [CODE] `evals/evals.json` contains concrete Drive MCP cases with `assets`, `deterministic_scripts`, and `quality_criteria` checks.
- [CODE] `examples/example-input.md` and `examples/example-output.md` are Drive-specific and no longer scaffold placeholders.

## Source Evidence

- [DOC] Local MCP setup: `docs/google-workspace-mcp-setup.md` documents `workspace-mcp`, Drive tools, read-only mode, and service-level permissions.
- [DOC] Local MCP integration: `docs/mcp-integration.md` documents project `.mcp.json`, `workspace-mcp`, and secret-handling guidance.
- [DOC] Google Drive scopes: https://developers.google.com/workspace/drive/api/guides/api-specific-auth
- [DOC] Google Drive search: https://developers.google.com/drive/api/guides/search-files
- [DOC] Google Drive `files.list`: https://developers.google.com/drive/api/reference/rest/v3/files/list
- [DOC] Google Drive uploads: https://developers.google.com/drive/api/v3/manage-uploads
- [DOC] Google Drive `files.create`: https://developers.google.com/drive/api/reference/rest/v3/files/create
- [DOC] Google Drive REST v3 overview: https://developers.google.com/drive/api/reference/rest/v3
- [DOC] Google Drive download/export: https://developers.google.com/workspace/drive/api/guides/manage-downloads
- [DOC] Google Drive MIME/export: https://developers.google.com/workspace/drive/api/guides/ref-export-formats
- [DOC] Google Drive supported MIME types: https://developers.google.com/workspace/drive/api/guides/mime-types
- [DOC] Google Drive sharing permissions: https://developers.google.com/workspace/drive/api/guides/manage-sharing
- [DOC] MCP tools spec: https://modelcontextprotocol.io/specification/draft/server/tools

## Validation Commands

```bash
python3 -B scripts/validate-skill-dod.py --skill google-drive-mcp
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill google-drive-mcp
bash skills/google-drive-mcp/scripts/check.sh
python3 -m py_compile skills/google-drive-mcp/scripts/compile-google-drive-mcp.py
git diff --check
```

## Residual Limits

- [INFERENCE] This review certifies the `google-drive-mcp` skill only.
- [INFERENCE] The deterministic script validates a plan/checklist contract; it does not prove live Drive access, file existence, OAuth scope grant, or MCP server availability.
- [INFERENCE] Live sharing remains dependent on user confirmation, file capabilities, Workspace admin policy, Shared Drive restrictions, and recipient correctness.
