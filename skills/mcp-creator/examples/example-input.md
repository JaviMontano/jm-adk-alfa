# Example Input

Create a deterministic MCP configuration plan for a local PostgreSQL server.

- server name: `postgres-local`
- transport: `stdio`
- command: `npx`
- args: `-y`, `@modelcontextprotocol/server-postgres`, `${DATABASE_URL}`
- scope: `local`
- auth: database URL from env var only
- existing config was read; no name collision found
- live connection test must be deferred until the user approves setup
