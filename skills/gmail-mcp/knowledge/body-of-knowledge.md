# Gmail MCP Body of Knowledge

## Canon

- [CODE] `gmail-mcp` operates through the local `workspace-mcp` server configured in `.mcp.json`.
- [CODE] The local setup guide documents Gmail tools for search, send, drafts, labels, and filters.
- [CODE] The local setup guide documents permission tiers: `readonly`, `organize`, `drafts`, `send`, and `full`.
- [CODE] The skill default is read-only-first: search/list before content reads, draft before send, confirm before risky mutation.
- [CODE] The offline compiler uses `assets/` JSON contracts and never calls Gmail, OAuth, network, or MCP.

## Gmail API Documentation Snapshot

- [DOC] The Gmail REST overview exposes `users.drafts`, `users.labels`, `users.messages`, `users.messages.attachments`, `users.settings.filters`, and `users.threads` resources.
- [DOC] Gmail API search uses `messages.list` or `threads.list` with the `q` parameter and can also filter by `labelIds[]`.
- [DOC] Gmail API search supports most Gmail web advanced search syntax, but the API can differ from the UI for alias expansion and thread-wide search.
- [DOC] Gmail API date strings in search are interpreted at PST midnight; Unix seconds are safer when timezone precision matters.
- [DOC] `users.messages.send` sends the specified message to recipients in `To`, `Cc`, and `Bcc`.
- [DOC] `users.messages.send` requires one of `https://mail.google.com/`, `gmail.modify`, `gmail.compose`, or `gmail.send`.
- [DOC] Google recommends choosing the most narrowly focused scope possible and avoiding unneeded scopes.
- [DOC] `gmail.labels` can see and edit labels; `gmail.send` sends mail; `gmail.metadata`, `gmail.readonly`, `gmail.compose`, and `gmail.modify` are broader or restricted scopes.
- [DOC] Gmail labels are either reserved `SYSTEM` labels or custom `USER` labels.
- [DOC] Labels cannot be applied to draft messages.

## Minimum Scope Heuristics

| Operation | Default Scope Review | Notes |
|---|---|---|
| Search metadata | `gmail.metadata` | Prefer `q`, `labelIds[]`, and bounded results. |
| Read message/thread body | `gmail.readonly` | Fetch only selected IDs. |
| List/manage label catalog | `gmail.labels` | Check system label name conflicts. |
| Create/update draft | `gmail.compose` | Draft before send. |
| Send approved message | `gmail.send` | Human confirmation required. |
| Modify labels on messages | `gmail.modify` | Bulk and visibility changes require confirmation. |
| Manage filters | explicit settings scope review | High-risk; confirm exact mutation first. |

## Deterministic Guards

| Failure | Guard |
|---|---|
| Direct send without approval | Reject unless confirmation starts with `CONFIRMED:`. |
| Broad content access | Search metadata first and fetch selected IDs only. |
| Bulk label surprise | Require confirmation when more than one message is affected. |
| System label collision | Reject custom labels named like Gmail system labels. |
| Draft label mutation | Block because Gmail labels cannot be applied to drafts. |
| Credential leakage | Never read or store OAuth tokens or credential files. |
| Attachment leakage | Keep attachment handling metadata-only unless explicitly requested. |

## Quality Metrics

| Metric | Target | How to Measure |
|---|---|---|
| Read-only-first coverage | 100% risky workflows | Compiler validation and review checklist. |
| Confirmation coverage | 100% for send/delete/filter/bulk-label | Compiler validation. |
| Scope review coverage | 100% planned actions | `assets/scope-matrix.json`. |
| Privacy storage | 0 message bodies or attachments in repo | Compiler validation and review. |
| Determinism | Stable output for same JSON | `scripts/check.sh` fixture. |
