# Google Drive MCP Meta Prompt

Review whether `google-drive-mcp` should activate, whether the Drive operation is
safe, and which support agents should participate.

## Activation Check

- Trigger match: Drive, Google Drive, upload, download, export, folder, search,
  share, permission, MIME type, or `workspace-mcp`.
- Domain fit: file/folder work in Google Drive, not Docs/Sheets/Slides content
  editing.
- Sufficient input: at least target, operation, and safety constraints. If a
  mutation is requested, confirmation must be obtained before execution.
- Safer specialized skill: route document editing to `google-docs-mcp`, sheet
  edits to `google-sheets-mcp`, and deck edits to `google-slides-mcp`.

## Safety Gates

- Read-only-first is required.
- Broad sharing (`domain`, `anyone`) requires explicit reason and confirmation.
- Full `drive` scope requires justification.
- Scripts under `scripts/` are offline compilers only.
