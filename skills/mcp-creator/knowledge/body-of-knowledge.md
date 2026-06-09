# MCP Creator Body of Knowledge

## Canon

`mcp-creator` validates configuration plans before live setup. It does not require network access, OAuth, or installed server packages to validate a plan. Live commands such as `claude mcp list`, OAuth browser flows, or server health checks are deferred until the user approves setup.

## Deterministic Plan Fields

| Field | Requirement |
|---|---|
| `server.name` | Kebab-case and unique across reviewed scopes |
| `transport.type` | `stdio` or `http`; `sse` is blocked |
| `scope.type` | `local`, `project`, `user`, or `plugin` |
| `auth.secrets_hardcoded` | Must be `false` |
| `preflight.existing_config_reviewed` | Must be `true` |
| `rollback.remove_command` | Required before apply |
| `validation.offline` | Must be `true` |

## Safety Invariants

- Use env-var placeholders for secrets.
- Do not write `.mcp.json` or user config during planning.
- Do not validate by reaching live remote systems unless explicitly approved.
- Treat project scope as shared and potentially tracked.
- Require rollback instructions before apply.

## Quality Signals

| Signal | Target |
|---|---|
| Transport correctness | Stdio has command/args; HTTP has HTTPS URL |
| Secret safety | No hardcoded tokens, keys, passwords, or bearer values |
| Scope safety | Config path and tracked-file risk match scope |
| Preflight | Existing config reviewed and name collision checked |
| Validation | Assets, deterministic scripts, evidence, and rollback are present |
