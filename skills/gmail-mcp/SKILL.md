---
name: gmail-mcp
author: JM Labs (Javier Montano)
version: 1.0.0
description: >
  Gmail operations through the local workspace-mcp server: search, read,
  draft, label, filter, and send workflows with read-only-first execution,
  least-scope review, privacy controls, and human confirmation for risky
  mutations. Trigger: "gmail", "email", "check inbox", "draft reply",
  "send email", "label messages", "Gmail MCP".
status: production
tags: [mcp, gmail, email, google-workspace, privacy, automation]
mcp-server: workspace-mcp
allowed-tools:
  - Read
  - Write
  - Bash
  - mcp__workspace-mcp__search_gmail_messages
  - mcp__workspace-mcp__get_gmail_message_content
  - mcp__workspace-mcp__get_gmail_messages_content_batch
  - mcp__workspace-mcp__send_gmail_message
  - mcp__workspace-mcp__get_gmail_thread_content
  - mcp__workspace-mcp__modify_gmail_message_labels
  - mcp__workspace-mcp__list_gmail_labels
  - mcp__workspace-mcp__manage_gmail_label
  - mcp__workspace-mcp__manage_gmail_filter
  - mcp__workspace-mcp__list_gmail_filters
  - mcp__workspace-mcp__draft_gmail_message
---

# Gmail MCP

## TL;DR

Use this skill for Gmail work through the local `workspace-mcp` server when the task needs search, message/thread reading, drafts, safe sending, labels, or filters. [CODE]

The default operating model is read-only-first: search or inspect metadata before reading bodies, draft before send, and require explicit human confirmation for send, delete/trash, filter mutation, or bulk label changes. [CODE]

For deterministic planning, use `scripts/compile-gmail-mcp.py` with JSON input and the assets under `assets/`; the script is offline-only and never calls Gmail, OAuth, or MCP. [CODE]

## Source Baseline

- [DOC] Local MCP setup: `docs/google-workspace-mcp-setup.md`.
- [DOC] Local MCP integration: `docs/mcp-integration.md`.
- [DOC] Google Gmail API REST overview: `https://developers.google.com/workspace/gmail/api/reference/rest`.
- [DOC] Google Gmail scopes: `https://developers.google.com/workspace/gmail/api/auth/scopes`.
- [DOC] Google `users.messages.send`: `https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.messages/send`.
- [DOC] MCP tools spec: `https://modelcontextprotocol.io/specification/draft/server/tools`.

## Procedure

### Step 1: Discover Safely

- [CODE] Confirm the task is really Gmail-specific and identify whether it is read-only, draft-only, send-capable, label-capable, or filter-capable.
- [CODE] Check current MCP configuration only when needed; `.mcp.json` configures `workspace-mcp` through `uvx workspace-mcp --tool-tier extended`.
- [DOC] Prefer `--read-only` or service permissions such as `gmail:readonly`, `gmail:drafts`, or `gmail:send` when the local MCP server is configured for a narrower run.
- [CODE] Do not read credentials, token files, or message bodies unless the user task requires that level of access.

### Step 2: Search Before Content

- [DOC] Gmail API search uses `messages.list` or `threads.list` with `q` and can also filter with `labelIds[]`.
- [DOC] Gmail API search supports most Gmail advanced search syntax, but Gmail UI alias expansion and thread-wide search behavior can differ.
- [DOC] Date strings in Gmail API search are interpreted at PST midnight; use Unix seconds when timezone precision matters.
- [CODE] Start with narrow queries such as `from:`, `subject:`, `after:`, `before:`, `newer_than:`, `label:`, `in:`, `is:`, or `has:attachment`.
- [CODE] Fetch message or thread content only after selecting concrete IDs from search results.

### Step 3: Review Scopes Before Tool Calls

- [DOC] Google recommends choosing the most narrowly focused scope possible and avoiding scopes an app does not require.
- [DOC] `gmail.labels` can see/edit labels; `gmail.send` sends mail; `gmail.metadata`, `gmail.readonly`, `gmail.compose`, and `gmail.modify` are broader or restricted Gmail scopes.
- [CODE] Use `assets/scope-matrix.json` before any live MCP operation.
- [CODE] Scope defaults by operation:
  - metadata search: `gmail.metadata`
  - message/thread body read: `gmail.readonly`
  - label catalog CRUD: `gmail.labels`
  - draft creation/update: `gmail.compose`
  - approved send: `gmail.send`
  - message label application or read/write organization: `gmail.modify`

### Step 4: Draft And Confirm

- [DOC] Gmail `users.messages.send` sends to recipients in `To`, `Cc`, and `Bcc`, accepts a `Message` request body, and requires one of the documented send-capable scopes.
- [DOC] Raw Gmail API sending uses MIME content encoded as base64URL; MCP tools may abstract the encoding, but the safety review still checks recipients and content.
- [CODE] Prefer `mcp__workspace-mcp__draft_gmail_message` for outbound email before `mcp__workspace-mcp__send_gmail_message`.
- [CODE] Before any send, show recipients, cc, bcc, subject, body summary, thread context, attachments, scope, and tool name.
- [CODE] Do not send unless the user explicitly confirms the exact send action.

### Step 5: Labels And Filters

- [DOC] Gmail labels are `SYSTEM` or `USER`; system label names are reserved.
- [DOC] Labels cannot be applied to draft messages.
- [DOC] Message label changes use message/thread modify semantics, while label catalog changes use label resources.
- [CODE] Confirm any label operation that affects more than one message, removes `INBOX`, adds `TRASH`, or otherwise changes visibility.
- [CODE] Treat filter mutation as high risk; require explicit user request, scope review, and human confirmation.

### Step 6: Validate And Report

- [CODE] Return a compact result with evidence tags, query/tool IDs, confirmation state, privacy controls, and residual risks.
- [CODE] Never paste full email bodies, credentials, tokens, or attachment payloads into repo files or logs.
- [CODE] When changing this skill, run `scripts/check.sh` plus the repo skill validators.

## Deterministic Resources

- [CODE] `assets/gmail-mcp-schema.json` defines the structured compiler input.
- [CODE] `assets/operation-safety-policy.json` defines read-only-first and confirmation gates.
- [CODE] `assets/scope-matrix.json` maps operations to Gmail scope review.
- [CODE] `assets/search-query-patterns.json` defines safe search patterns and date caveats.
- [CODE] `assets/label-policy.json` defines label safety rules.
- [CODE] `assets/send-draft-policy.json` defines draft-first and send-confirmation rules.
- [CODE] `assets/privacy-redaction-policy.json` defines redaction and non-storage rules.
- [CODE] `scripts/compile-gmail-mcp.py` compiles an offline plan/checklist from JSON.

## Quality Criteria

- [ ] Search or list operation precedes body read, draft, send, label mutation, or filter mutation.
- [ ] Scope review names the minimum Gmail scope family for every planned operation.
- [ ] Send, delete/trash, filter mutation, and bulk label mutation have explicit human confirmation.
- [ ] Draft-first flow is used unless the user explicitly requests and confirms direct send.
- [ ] Email bodies, attachments, OAuth tokens, and credentials are not stored in the repository.
- [ ] Evidence tags are present for claims and decisions.
- [ ] Offline compiler and fixtures pass before marking the skill DoD-complete.

## Anti-Patterns

- Sending email without a fresh user confirmation.
- Reading message bodies when metadata or headers are enough.
- Running broad inbox searches with high result counts.
- Storing email content, attachments, OAuth tokens, credentials, or private addresses in repo artifacts.
- Creating labels that collide with Gmail system labels.
- Mutating filters or bulk labels from a natural-language summary without showing the exact action.
- Requesting `https://mail.google.com/` unless a documented exception proves that narrower scopes are insufficient.

## Tool Reference

| Tool | Safe Use |
|---|---|
| `mcp__workspace-mcp__search_gmail_messages` | Search metadata first with narrow Gmail query syntax. |
| `mcp__workspace-mcp__get_gmail_message_content` | Read one selected message after search. |
| `mcp__workspace-mcp__get_gmail_messages_content_batch` | Read a bounded batch after IDs are selected and body access is justified. |
| `mcp__workspace-mcp__get_gmail_thread_content` | Read a selected conversation thread. |
| `mcp__workspace-mcp__draft_gmail_message` | Create a reviewable draft; preferred before send. |
| `mcp__workspace-mcp__send_gmail_message` | Send only after explicit human confirmation. |
| `mcp__workspace-mcp__list_gmail_labels` | Inspect label catalog before label changes. |
| `mcp__workspace-mcp__manage_gmail_label` | Create/update/delete labels after reserved-name checks. |
| `mcp__workspace-mcp__modify_gmail_message_labels` | Apply/remove labels after confirmation when bulk or visibility-changing. |
| `mcp__workspace-mcp__list_gmail_filters` | Inspect filter configuration. |
| `mcp__workspace-mcp__manage_gmail_filter` | Mutate filters only with explicit confirmation and scope review. |

## Usage

- `/gmail-mcp` - Plan or perform a safe Gmail operation.
- `Search Gmail for unread invoices from May and summarize only the selected threads.`
- `Draft a reply to the latest P-007 message, but do not send.`
- `Label these three messages as Project/P-007 after I approve the exact IDs.`
- `Send this approved reply to Ana after showing me recipients, subject, and body summary.`

## Assumptions & Limits

- [CONFIG] This repo configures the local Google Workspace MCP server as `workspace-mcp`.
- [INFERENCE] Live Gmail operations depend on local OAuth state, enabled Gmail API, and the active MCP permission tier.
- [CODE] The deterministic script renders plans only; it does not call Gmail, OAuth, or MCP.
- [INFERENCE] A safe plan is not proof that a live Gmail account contains matching messages.
