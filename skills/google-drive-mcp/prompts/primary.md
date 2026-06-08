# Google Drive MCP Primary Prompt

## Objective

Plan or execute safe Google Drive work through `workspace-mcp`.

## Required Inputs

- Goal
- Drive target context: file name, folder path, file ID, Shared Drive, or query
- Constraints
- Intended operation: search/list, upload, download/export, folder organization,
  copy/update, or sharing/permissions
- Definition of done and confirmation requirements

## Process

1. Discover read-only first with search/list or metadata inspection.
2. Build explicit Drive parameters: `q`, `fields`, `trashed = false`, `spaces`,
   `corpora`, page size, MIME/export type, and scope profile.
3. Confirm before any upload, folder creation, copy/update, or permission change.
4. Execute only the minimum MCP tool calls needed.
5. Validate with evidence and residual limits.

## Output

Return Markdown with summary, evidence, MCP preflight, operation plan, validation,
and risks. Use `scripts/compile-google-drive-mcp.py` for structured offline
plans.
