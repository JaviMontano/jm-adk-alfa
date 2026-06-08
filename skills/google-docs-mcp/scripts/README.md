# Google Docs MCP Scripts

## `compile-google-docs-mcp.py`

Compiles a structured JSON request into an offline Google Docs MCP plan. The
script validates local schema, scope policy, MCP tool mapping, Docs API method
selection, and human-confirmation requirements.

The script does not call Google Docs, OAuth, or MCP tools.

## Checks

Run from the repository root:

```bash
bash skills/google-docs-mcp/scripts/check.sh
```

The check validates one positive fixture and three negative fixtures:

- missing mutation confirmation
- invalid `documents.create` body content
- `documents.batchUpdate` without a prior `documents.get`
