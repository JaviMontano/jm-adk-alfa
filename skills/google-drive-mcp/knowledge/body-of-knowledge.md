# Google Drive MCP Body of Knowledge

## Canon

`google-drive-mcp` is the safe Drive operations skill for the local
`workspace-mcp` server. It covers search/list, upload, download/export, folder
organization, and sharing/permissions. The canonical deterministic resources are
under `assets/`; the offline compiler is
`scripts/compile-google-drive-mcp.py`.

## Primary Source Rules

- [DOC] Local MCP setup comes from `docs/google-workspace-mcp-setup.md` and
  `docs/mcp-integration.md`.
- [DOC] Drive API behavior comes from official Google Drive API docs only:
  scopes, search, `files.list`, upload file data, `files.create`, REST v3,
  download/export, MIME/export, and sharing permissions.
- [DOC] MCP safety behavior comes from the official MCP tools specification.
- [INFERENCE] When a local MCP tool abstracts a Drive REST call, preserve the
  Drive REST safety concept in the plan: read-only discovery, narrow fields,
  least privilege, capability checks, and explicit confirmation.

## Drive Search And Listing

- [DOC] Use `q` for filtering and include `trashed = false` unless the user is
  explicitly searching trash.
- [DOC] Use `fields` to return only needed metadata such as IDs, names, MIME
  types, parents, web links, and relevant capabilities.
- [DOC] Prefer `corpora=user` for My Drive and `corpora=drive` with a Shared
  Drive ID when known. Use `allDrives` only with a reason.
- [DOC] Use `spaces=drive` for ordinary Drive files.
- [CODE] Query policy is captured in `assets/query-policy.json`.

## Scopes And Permission Profiles

- [DOC] Google recommends the most narrowly focused scope possible.
- [DOC] `drive.file` is the preferred non-sensitive profile for files created by
  the app or explicitly opened/shared with the app.
- [DOC] `drive.metadata.readonly` is metadata-only and cannot download file
  content or mutate Drive resources.
- [DOC] `drive.readonly` can view/download accessible files but cannot mutate.
- [DOC] Full `drive` scope is restricted and should be justified before use.
- [CODE] Scope policy is captured in `assets/scope-policy.json`.

## Uploads

- [DOC] `uploadType=media` is for small media-only uploads without metadata.
- [DOC] `uploadType=multipart` is for small uploads with metadata in one request.
- [DOC] `uploadType=resumable` is required by this skill for files greater than
  5 MB and recommended when interruptions are likely.
- [CODE] Upload policy is captured in `assets/upload-policy.json`.

## Downloads, Exports, And MIME Types

- [DOC] Blob file content uses media download semantics.
- [DOC] Google Workspace documents use export to a supported MIME type such as
  PDF, DOCX, XLSX, PPTX, CSV, plain text, or Markdown.
- [DOC] Verify `capabilities.canDownload` before download/export.
- [CODE] Export MIME mappings are captured in `assets/mime-export-map.json`.

## Sharing And Permissions

- [DOC] Permission resources combine a `type` (`user`, `group`, `domain`,
  `anyone`) with a `role` (`reader`, `commenter`, `writer`, `fileOrganizer`,
  `organizer`, `owner`).
- [DOC] Check file capabilities, especially `canShare`, before sharing.
- [DOC] Folder permission changes can propagate to children.
- [CODE] Sharing policy is captured in `assets/sharing-permission-policy.json`.
- [INFERENCE] Any sharing or link-access change should be treated as high impact
  and require explicit human confirmation.

## MCP Practice

- [DOC] MCP tools are model-controlled, so applications should make tool
  exposure visible and present confirmation prompts for operations.
- [CODE] `assets/mcp-tool-contract.json` classifies Drive MCP tools as read-only
  or mutating.
- [CODE] Skill scripts are offline policy compilers only. They must not invoke
  Drive, OAuth, HTTP, or MCP.

## Quality Signals

| Signal | Target |
|---|---|
| Read-only-first | A search/list or other read-only verification precedes mutation |
| Query precision | `q`, `fields`, `trashed = false`, `spaces`, and efficient `corpora` are explicit |
| Scope control | Operation uses the narrowest viable scope profile |
| Upload correctness | Upload type follows size and metadata needs |
| Export correctness | Google Workspace files use supported export MIME types |
| Sharing safety | Capability check and human confirmation are explicit |
| Offline determinism | Scripts compile JSON to Markdown without network or MCP calls |
