# MCP Creator

Designs deterministic MCP server configuration plans before any live setup is attempted.

## Use When

- A user asks to configure, inspect, or plan an MCP server.
- A project needs a stdio or HTTP MCP config with scope and auth decisions.
- A proposed MCP setup needs validation before touching `.mcp.json`, user config, or plugin config.

## Do Not Use When

- The request is a one-off API call and no MCP server should be configured.
- The request asks to hardcode secrets, tokens, passwords, or OAuth credentials.
- The validation requires live network access before the user approves setup.

## Required Output

Return a JSON-compatible plan with:

- server name and collision-check evidence
- transport type and config
- scope decision and tracked-file risk
- auth policy with env-var placeholders
- preflight checks
- rollback plan
- evidence entries
- offline validation checks

## Validation

```bash
bash skills/mcp-creator/scripts/check.sh
python3 skills/mcp-creator/scripts/validate_mcp_config_plan.py skills/mcp-creator/scripts/fixtures/valid-stdio-postgres.json
```
