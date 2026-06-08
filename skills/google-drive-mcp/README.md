# Google Drive MCP

Use this skill to plan and execute safe Google Drive work through the local
`workspace-mcp` server: search/list, upload, download/export, folder
organization, copy/update, and sharing/permissions.

## Deterministic Resources

- `assets/google-drive-mcp-schema.json` defines the structured request contract.
- `assets/query-policy.json` captures Drive search/list defaults: explicit `q`,
  `fields`, `trashed = false`, efficient `corpora`, `spaces`, and page size.
- `assets/scope-policy.json` defines least-privilege scope profiles, including
  `drive.file`, `drive.readonly`, and `drive.metadata.readonly`.
- `assets/upload-policy.json` maps upload intent to `uploadType=media`,
  `uploadType=multipart`, or `uploadType=resumable`.
- `assets/sharing-permission-policy.json` defines permission types, roles,
  capability checks, and human-confirmation gates.
- `assets/mime-export-map.json` maps Google Workspace MIME types to export MIME
  types and file extensions.
- `assets/mcp-tool-contract.json` maps local `workspace-mcp` tools to read-only
  or mutating Drive operations.
- `scripts/compile-google-drive-mcp.py` renders an offline Markdown plan and
  checklist from JSON. It does not call Google Drive, OAuth, or MCP tools.

## Output Format

Markdown with evidence, MCP preflight, operation plan, search/list contract,
upload/download/export decisions, permission confirmation gates, validation, and
residual risks.
