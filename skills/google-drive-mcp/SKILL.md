---
name: google-drive-mcp
author: JM Labs (Javier Montano)
version: 1.0.0
description: >
  Google Drive integration via MCP — upload, download, organize, search, and share
  files and folders. [EXPLICIT]
  Trigger: "drive", "google drive", "upload file", "share file", "drive search"
status: production
tags: [mcp, google-drive, files, storage, automation, google]
mcp-server: workspace-mcp
allowed-tools:
  - Read
  - Write
  - Bash
  - mcp__workspace-mcp__search_drive_files
  - mcp__workspace-mcp__get_drive_file_content
  - mcp__workspace-mcp__create_drive_file
  - mcp__workspace-mcp__create_drive_folder
  - mcp__workspace-mcp__list_drive_items
  - mcp__workspace-mcp__copy_drive_file
  - mcp__workspace-mcp__update_drive_file
  - mcp__workspace-mcp__manage_drive_access
  - mcp__workspace-mcp__get_drive_shareable_link
---

# Google Drive MCP

## TL;DR

Plan and execute Google Drive work through the local `workspace-mcp` server with
read-only discovery before mutation. Use this skill for Drive search/list,
upload, download/export, folder organization, copy/update, and
sharing/permissions. Use `scripts/compile-google-drive-mcp.py` when the request
can be represented as structured JSON and a reproducible offline checklist is
useful. [EXPLICIT]

## Prerequisites

- Google Workspace MCP server configured (see `docs/google-workspace-mcp-setup.md`)
- Google Drive API enabled and OAuth credentials authenticated through the local
  `workspace-mcp` setup
- Drive operations scoped to the narrowest available permission profile:
  prefer `drive.file` for created/opened files, `drive.metadata.readonly` for
  metadata-only discovery, and `drive.readonly` only when full read/download
  access is necessary

## Procedure

### Step 1: Discover Read-Only
- Confirm `.mcp.json` exposes `workspace-mcp` with Drive tools before using MCP.
- Use `mcp__workspace-mcp__search_drive_files` or
  `mcp__workspace-mcp__list_drive_items` before any upload, folder creation,
  copy/update, or sharing change.
- Make Drive search explicit: include a `q` query, `trashed = false`, `fields`,
  `spaces=drive`, and efficient `corpora` (`user` or a specific `drive` before
  `allDrives`).
- Request only useful fields such as `files(id,name,mimeType,parents,webViewLink,
  capabilities/canDownload,capabilities/canShare)` and `nextPageToken`.

### Step 2: Select Scope And Operation Mode
- Use `assets/scope-policy.json` to choose the least-privilege scope profile.
- Treat `drive.file` as the preferred mutation profile for files created or
  selected for the app; do not escalate to full `drive` unless the task truly
  requires account-wide mutation.
- Treat metadata-only lookup as `drive.metadata.readonly`; treat download/export
  of all accessible files as `drive.readonly`.
- Keep the offline compiler in `scripts/` for plan generation only. It must not
  call Drive, OAuth, or MCP.

### Step 3: Plan File And Folder Work
- For uploads, choose `uploadType=media` for small media-only uploads,
  `uploadType=multipart` for small uploads with metadata, and
  `uploadType=resumable` for files greater than 5 MB or interruption-prone
  uploads.
- For downloads, distinguish blob files from Google Workspace files: blob content
  uses media download semantics, while Google Docs/Sheets/Slides use export MIME
  types such as PDF, DOCX, XLSX, PPTX, CSV, or Markdown.
- For folders, use `application/vnd.google-apps.folder`, verify the parent, and
  check inherited sharing before creating or moving content.

### Step 4: Confirm Mutations
- Ask for human confirmation before upload, folder creation, copy/update, or
  permission changes.
- For sharing, verify `capabilities.canShare`, permission `type`, role, email or
  domain target, notification behavior, expiration if applicable, and whether
  link/domain/anyone access is being introduced.
- Avoid broad `anyone` or domain-level sharing unless the user explicitly
  confirms recipient, role, duration, and business reason.

### Step 5: Validate And Report
- Return evidence-tagged output with source of truth, selected MCP tool, query or
  upload/export parameters, confirmation state, and residual limits.
- Run `scripts/check.sh` when changing this skill.

## Quality Criteria

- [ ] Read-only discovery happens before mutating Drive actions
- [ ] Search/list requests include `q`, `fields`, `trashed = false`, `spaces`, and
      efficient `corpora`
- [ ] OAuth scope profile is least privilege for the requested operation
- [ ] Upload plan selects `media`, `multipart`, or `resumable` from file size and
      metadata needs
- [ ] Download/export plan distinguishes blob content from Google Workspace
      document export
- [ ] Folder operations verify parent, MIME type, and inherited permission impact
- [ ] Sharing/permission changes include human confirmation and capability checks
- [ ] Scripts stay offline and deterministic; no Drive, OAuth, or MCP calls
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Deleting files without user confirmation
- Running a mutating MCP tool before search/list discovery
- Searching without `trashed = false`, partial `fields`, or an efficient corpus
- Sharing with `anyone` or a whole domain without explicit confirmation
- Uploading credentials, tokens, `.env`, or private local state to Drive
- Treating Google Workspace documents as blob downloads instead of exports
- Using full `drive` scope when `drive.file`, `drive.readonly`, or
  `drive.metadata.readonly` is sufficient
- Deep recursive folder moves without a count, parent, and inherited-permission
  review

## Related Skills

- `google-docs-mcp` — edit Google Docs content
- `google-sheets-mcp` — read/write spreadsheet data
- `google-slides-mcp` — create presentations
- `google-workspace-apis` — programmatic Drive API patterns

## Usage

- `/google-drive-mcp` — interactive Drive management
- "upload the report to my Drive in /Projects/Q2"
- "search Drive for presentation files from last month"
- "share the proposal folder with ana@company.com as editor"
- "compile a safe Drive MCP plan from this JSON fixture"

## Assumptions & Limits

- Requires authenticated local Google Workspace MCP server [EXPLICIT]
- Uses local assets under `assets/` for deterministic Drive API policy, not live
  Drive inspection [EXPLICIT]
- `scripts/compile-google-drive-mcp.py` renders a plan/checklist only; it does
  not call Drive, OAuth, or MCP [EXPLICIT]
- Real Drive outcomes depend on account access, OAuth scopes, Shared Drive
  policy, file capabilities, and user confirmation [EXPLICIT]
- Large files may take time to upload/download/export in real MCP execution
  [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or broad search | Request a narrower `q`, target corpus, fields, and page size before calling Drive |
| Shared Drive target | Use `corpora=drive`, `driveId`, and all-drive support flags when the MCP tool exposes them |
| Google Docs/Sheets/Slides download | Export to a supported MIME type instead of blob download |
| Permission mutation | Require human confirmation and verify `capabilities.canShare` first |
| Broad access request | Surface risk and ask for explicit recipient, role, expiry, and reason |
