# Example Input

Plan a Google Slides MCP workflow for a QBR deck.

Requirements:

- Read the template presentation `template_qbr_2026`.
- Read page `slide_title`.
- Generate a `MEDIUM` PNG thumbnail and discard the temporary `contentUrl` after review.
- Create a new presentation named `QBR Draft 2026`.
- Apply a `batchUpdate` that creates `slide_exec_summary` and inserts the title `Executive Summary`.
- Use the minimum viable scope profile.
- Require explicit human confirmation before the create and batchUpdate operations.
- Return an offline Markdown checklist before any live MCP tool call.
