# Example Output

## Summary

[CODE] Prepared a Gmail MCP plan for a read-only-first P-007 inbox workflow.

## Evidence

- [CODE] Source skill: `gmail-mcp`.
- [CODE] Deterministic assets used: `assets/scope-matrix.json`, `assets/operation-safety-policy.json`, `assets/send-draft-policy.json`, and `assets/privacy-redaction-policy.json`.
- [DOC] Gmail API search supports `q` and `labelIds[]`; the plan starts with metadata search before content access.
- [DOC] Google recommends narrow scopes; the plan reviews `gmail.metadata`, `gmail.readonly`, `gmail.compose`, `gmail.send`, and `gmail.modify` by operation.

## Scope Review

| Operation | Tool | Minimum Scope Review |
|---|---|---|
| Search messages | `mcp__workspace-mcp__search_gmail_messages` | `gmail.metadata` |
| Read selected thread | `mcp__workspace-mcp__get_gmail_thread_content` | `gmail.readonly` |
| Draft reply | `mcp__workspace-mcp__draft_gmail_message` | `gmail.compose` |
| Bulk label selected messages | `mcp__workspace-mcp__modify_gmail_message_labels` | `gmail.modify` |
| Send approved draft | `mcp__workspace-mcp__send_gmail_message` | `gmail.send` |

## Tool Sequence

1. [CODE] Search with `subject:"P-007" newer_than:14d -in:trash`, `labelIds[] = INBOX`, and max 10 results.
2. [CODE] Read only the selected thread ID from search results.
3. [CODE] Draft the reply and show recipients, subject, thread context, and body summary.
4. [CODE] Apply `Project/P-007` to selected message IDs only after confirmation because more than one message is affected.
5. [CODE] Send only after explicit human confirmation of recipients, subject, body summary, and send scope.

## Validation

- [CODE] Read-only-first gate: pass.
- [CODE] Draft-first gate: pass.
- [CODE] Send confirmation gate: pending user confirmation.
- [CODE] Bulk label confirmation gate: pending user confirmation.
- [CODE] Privacy gate: no email body, attachment, token, or credential storage.

## Risks and Limits

- [INFERENCE] The plan is safe to review offline, but live execution still depends on the active Gmail account and MCP permission tier.
- [INFERENCE] Search results can differ from Gmail UI behavior for alias expansion and thread-wide search.
