---
name: google-docs-mcp
author: JM Labs (Javier Montano)
version: 1.0.0
description: >
  Google Docs integration via MCP - create, inspect, and update documents through
  deterministic Docs API plans with human confirmation before mutation. [EXPLICIT]
  Trigger: "google doc", "create document", "edit doc", "document"
status: production
tags: [mcp, google-docs, documents, content, automation, google]
mcp-server: workspace-mcp
allowed-tools:
  - Read
  - Write
  - Bash
  - mcp__workspace-mcp__get_doc_content
  - mcp__workspace-mcp__create_doc
  - mcp__workspace-mcp__modify_doc_text
  - mcp__workspace-mcp__search_docs
  - mcp__workspace-mcp__find_and_replace_doc
  - mcp__workspace-mcp__insert_doc_elements
  - mcp__workspace-mcp__get_doc_as_markdown
  - mcp__workspace-mcp__export_doc_to_pdf
---

# Google Docs MCP

## TL;DR

Plan and execute Google Docs work through the local `workspace-mcp` server with
least-privilege scope selection and a hard human-confirmation gate before
`documents.create` or `documents.batchUpdate`. Use
`scripts/compile-google-docs-mcp.py` when the request can be represented as
structured JSON and a reproducible offline checklist is useful. [EXPLICIT]

## Prerequisites

- Google Workspace MCP server configured (see `docs/google-workspace-mcp-setup.md`)
- Google Docs API enabled and OAuth credentials authenticated through the local
  `workspace-mcp` setup
- Local reference assets available under `assets/` and deterministic checks under
  `scripts/`

## Procedure

### Step 1: Confirm Server And Scope
- Confirm `.mcp.json` exposes `workspace-mcp` with Docs tools before live use.
- Use `assets/scope-policy.json` to select the narrowest scope profile.
- Prefer `documents.readonly` for read-only inspection and `drive.file` for
  documents created or explicitly opened for the app.
- Escalate to full `documents` only with a written reason.

### Step 2: Create Or Resolve The Document
- Use `documents.create` only for a blank document with a title.
- Do not include body content in `documents.create`; insert initial content with a
  follow-up `documents.batchUpdate` request.
- Capture the created document ID before planning later operations.

### Step 3: Inspect Before Batch Update
- Use `documents.get` before editing an existing or newly created document.
- Request only useful fields, such as document ID, title, body content, tabs,
  and revision ID when the workflow needs safe writes.
- Capture current structure, indexes, and revision information before composing
  ranges for `documents.batchUpdate`.

### Step 4: Compose Batch Update Requests
- Use `documents.batchUpdate` for real Docs operations such as `insertText`,
  `deleteContentRange`, `replaceAllText`, `updateTextStyle`,
  `updateParagraphStyle`, `createParagraphBullets`, `insertTable`, and
  `insertPageBreak`.
- Include `writeControl.requiredRevisionId` when a prior `documents.get` captured
  a revision ID.
- Keep request order explicit because batch-update requests are applied in the
  order provided by the API.

### Step 5: Confirm Mutations And Validate
- Ask for human confirmation before any `documents.create` or
  `documents.batchUpdate` operation.
- Report selected MCP tool, Docs API method, scope profile, confirmation state,
  request checklist, validation result, and residual limits.
- Run `scripts/check.sh` when changing this skill.

## Quality Criteria

- [ ] Operation plan uses real Docs API methods: `documents.create`,
      `documents.get`, and `documents.batchUpdate`
- [ ] `documents.create` remains title-only; body content is inserted by
      `documents.batchUpdate`
- [ ] Existing document edits include a prior `documents.get` inspection step
- [ ] Batch update requests use stable request objects and explicit ordering
- [ ] Mutations have human confirmation before live MCP execution
- [ ] OAuth scope profile is least privilege for the requested operation
- [ ] Scripts stay offline and deterministic; no Docs, OAuth, or MCP calls
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Inserting body content directly into `documents.create`
- Running `documents.batchUpdate` without a prior `documents.get`
- Mutating a document without an explicit human-confirmation record
- Using full `documents` scope when `documents.readonly` or `drive.file` is enough
- Guessing text indexes instead of reading document structure first
- Overwriting entire documents when scoped batch-update requests are sufficient
- Treating export as proof that a live edit succeeded

## Related Skills

- `google-drive-mcp` - file search, sharing, and export boundaries
- `google-sheets-mcp` - spreadsheet data workflows
- `google-slides-mcp` - presentation creation and updates
- `google-workspace-apis` - programmatic Google Workspace API patterns

## Usage

- `/google-docs-mcp` - interactive document management
- "create a Google Doc with these meeting notes"
- "inspect this document and plan a safe batch update"
- "compile a Docs MCP plan from this JSON fixture"

## Assumptions & Limits

- Requires authenticated local Google Workspace MCP server [EXPLICIT]
- Uses local assets under `assets/` for deterministic Docs API policy, not live
  Google Docs inspection [EXPLICIT]
- `scripts/compile-google-docs-mcp.py` renders a plan/checklist only; it does
  not call Docs, OAuth, or MCP [EXPLICIT]
- Real Docs outcomes depend on account access, OAuth scopes, document ACLs,
  current revision state, and user confirmation [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| User asks to create a document with content | Plan `documents.create` for the title, then `documents.batchUpdate` for content |
| Existing document edit | Require `documents.get` before batch-update index or style requests |
| Unknown indexes | Stop and inspect structure before generating ranges |
| Broad scope request | Surface risk and require a written escalation reason |
| Mutation requested without confirmation | Return a confirmation checklist instead of calling mutating tools |
