# Gmail MCP Scripts

- `compile-gmail-mcp.py` validates structured JSON and renders an offline Gmail MCP operation plan.
- `check.sh` runs the positive fixture, expected-fragment checks, and invalid-input failure checks.

These scripts never call Gmail, Google APIs, OAuth, or the live MCP server.
