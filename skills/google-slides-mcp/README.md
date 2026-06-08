<!--
generated-by: scripts/scaffold-skill.py
generated-for: google-slides-mcp
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Google Slides MCP

Deterministic Google Slides skill for planning `workspace-mcp` work against the Slides REST API.

## Triggers

- google-slides-mcp
- google slides
- slides deck
- presentation automation
- slide thumbnail
- batchUpdate presentation

## Allowed Tools

- Read
- Write
- Bash
- mcp__workspace-mcp__create_presentation
- mcp__workspace-mcp__get_presentation
- mcp__workspace-mcp__batch_update_presentation
- mcp__workspace-mcp__get_page
- mcp__workspace-mcp__get_page_thumbnail

## Quick Use

1. Start offline with `scripts/compile-google-slides-mcp.py`.
2. Validate operation order, scope profile, payload shape, and human-confirmation gates.
3. Use live MCP tools only after the offline checklist is clean.

## Deterministic Check

```bash
bash skills/google-slides-mcp/scripts/check.sh
```

## Output Format

Markdown with summary, evidence, MCP preflight, operation table, scope review, payload preview, validation, and risks. HTML fallback lives in `templates/output.html`.
