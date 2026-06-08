# Google Slides MCP Meta Prompt

Review whether `google-slides-mcp` should activate, whether the scope is safe, and whether live MCP execution is permitted.

## Activation Check

- Activate for Google Slides decks, presentations, pages, thumbnails, or Slides REST/MCP workflows.
- Activate for `presentations.create`, `presentations.get`, `presentations.batchUpdate`, `presentations.pages.get`, or `presentations.pages.getThumbnail`.
- Do not activate for Docs, Sheets, Drive-only file organization, or generic presentation advice without Google Slides execution.

## Safety Gate

- Block mutation if human confirmation is missing or vague.
- Block broad Drive scopes unless `scope_exception.reason` is explicit.
- Block `batchUpdate` if the target presentation was not read first or created in the same plan.
- Block durable persistence of thumbnail `contentUrl`.
