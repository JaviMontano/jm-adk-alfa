# Gmail MCP Meta Prompt

Review whether `gmail-mcp` should activate and whether the operation is safe.

## Activation Check

- Trigger mentions Gmail, inbox, email search, draft, send, labels, filters, or a Gmail MCP tool.
- Task requires the local `workspace-mcp` Gmail service rather than generic email copywriting.
- User has provided enough mailbox/query/action context, or the next step can be a read-only discovery query.
- No safer specialized skill owns the request.

## Safety Check

- Read-only-first is possible.
- Minimum scope can be named before tool use.
- Send/delete/trash/filter/bulk-label confirmation is explicit.
- Email bodies, attachments, credentials, and tokens will not be persisted.
- Live MCP execution is separated from offline script validation.
