# Google Docs MCP Meta Prompt

Review whether `google-docs-mcp` should activate, whether the requested Docs
operation is safe, and which agent lens should lead.

## Activation Check

- Trigger references Google Docs, document creation, document inspection, or
  document editing.
- The work can be represented by `documents.create`, `documents.get`,
  `documents.batchUpdate`, or a local `workspace-mcp` Docs tool.
- The request is not better handled by Drive, Sheets, Slides, Gmail, or Calendar.

## Safety Check

- Read-only inspection may proceed with read-only tooling and least privilege.
- `documents.create` and `documents.batchUpdate` require confirmation before live
  execution.
- Batch updates require a prior `documents.get` for the same document.
- Broad `documents` scope requires escalation reason.

## Agent Routing

- Lead handles operation planning and output.
- Support reviews request ordering, indexes, styling, and scope.
- Guardian blocks missing evidence, missing confirmation, or unsafe scope.
- Specialist joins for tables, styles, bullets, and rich content requests.
