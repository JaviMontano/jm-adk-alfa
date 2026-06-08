# Example Output

## Summary

- [CODE] MCP server: `workspace-mcp`.
- [CODE] Mode: `safe_execution_checklist`.
- [CODE] First operation: read-only Drive search.
- [CODE] Mutating operations require human confirmation before live MCP calls.

## Search And List Contract

- [CODE] q: `name contains 'alfa' and trashed = false`.
- [CODE] fields: `nextPageToken, files(id, name, mimeType, parents, size, modifiedTime, webViewLink, capabilities/canDownload, capabilities/canShare)`.
- [CODE] corpora: `user`.
- [CODE] spaces: `drive`.
- [CODE] page size: 25.

## Operation Plan

| ID | Action | MCP Tool | Safety Gate |
|---|---|---|---|
| discover-alpha-assets | search_list | `mcp__workspace-mcp__search_drive_files` | read-only |
| create-alpha-folder | organize_folder | `mcp__workspace-mcp__create_drive_folder` | confirm before mutation |
| upload-alpha-report | upload | `mcp__workspace-mcp__create_drive_file` | confirm before mutation |
| export-source-brief | download_export | `mcp__workspace-mcp__get_drive_file_content` | verify `canDownload` |
| share-alpha-report | share_permission | `mcp__workspace-mcp__manage_drive_access` | verify `canShare` and confirm recipient/role |

## Drive API Decisions

- [DOC] Use `drive.metadata.readonly` for metadata discovery.
- [DOC] Use `drive.file` for per-file upload, folder creation, and sharing when
  the file is created or opened for the app.
- [DOC] Use `uploadType=multipart` for a small PDF upload with metadata.
- [DOC] Use export MIME type `application/pdf` for the Google Docs source brief.
- [DOC] Permission target is type `user`, role `commenter`,
  `reviewer@example.com`.

## Validation

- [CODE] The compiled plan includes `q`, `fields`, `trashed = false`, `spaces`,
  `corpora`, and page size.
- [CODE] Sharing requires `capabilities.canShare` and human confirmation.
- [CODE] The compiler performs no network, OAuth, Drive, or MCP calls.
