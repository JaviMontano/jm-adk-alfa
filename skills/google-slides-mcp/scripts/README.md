# Google Slides MCP Scripts

`compile-google-slides-mcp.py` validates a structured Google Slides MCP plan and renders a deterministic Markdown checklist. It is offline-only: it reads local JSON fixtures and `assets/` files, and it never calls Google Slides, OAuth, network, or MCP tools.

## Check

```bash
bash skills/google-slides-mcp/scripts/check.sh
```

## Fixture Contract

- Valid fixture: `fixtures/google-slides-mcp-input.json`
- Invalid fixture: `fixtures/invalid-missing-confirmation.json`
- Invalid fixture: `fixtures/invalid-broad-scope.json`
