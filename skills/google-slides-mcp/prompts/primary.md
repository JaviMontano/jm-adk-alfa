# Google Slides MCP Primary Prompt

## Objective

Produce a safe Google Slides MCP operation plan before live tool execution.

## Required Inputs

- Deck goal and audience.
- Target presentation IDs or creation title.
- Requested Slides operations.
- OAuth scope constraints.
- Human confirmation text for every mutation.
- Definition of done and validation needs.

## Process

1. Read `SKILL.md` and the relevant `assets/` policy files.
2. Convert the request into the stable JSON contract in `assets/google-slides-mcp-schema.json`.
3. Run or mirror `scripts/compile-google-slides-mcp.py` before any live MCP call.
4. Use read-only tools first: `get_presentation`, `get_page`, or `get_page_thumbnail`.
5. Use `create_presentation` or `batch_update_presentation` only after explicit confirmation.
6. Read back the presentation or page after mutation.

## Output

Return Markdown using `templates/output.md`: summary, evidence, MCP preflight, operation table, scope review, safety gates, payload preview, live checklist, validation, and risks.
