<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-mcp-server-configuration
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Input

Escenario Customer Support. El equipo necesita que todos los agentes Claude Code accedan al CRM via un MCP server. Un dev propone este `.mcp.json` para versionar en el repo:

```json
{
  "mcpServers": {
    "crm": {
      "command": "npx",
      "args": ["-y", "@acme/mcp-server-crm"],
      "env": { "CRM_TOKEN": "crm_live_7Hk29ZqPmN4xR" }
    }
  }
}
```

Pregunta: este server debe ir en `.mcp.json` o en `~/.claude.json`, y como se debe manejar el `CRM_TOKEN`?
