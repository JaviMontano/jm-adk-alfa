# Google Calendar MCP Scripts

The scripts in this directory are offline and deterministic. They never call Google Calendar, OAuth, or MCP tools.

## Compiler

```bash
python3 skills/google-calendar-mcp/scripts/compile-google-calendar-mcp.py \
  --input skills/google-calendar-mcp/scripts/fixtures/google-calendar-mcp-input.json \
  --output /tmp/google-calendar-mcp-plan.md
```

The compiler validates a structured Calendar operation against local assets and renders a safe Markdown plan.

## Check

```bash
bash skills/google-calendar-mcp/scripts/check.sh
```

The check validates positive and negative fixtures, expected output fragments, and strict offline failure modes.
