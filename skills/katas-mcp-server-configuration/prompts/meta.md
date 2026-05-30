<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-mcp-server-configuration
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Kata 22 · Meta Prompt · Chequeo de activacion

Decide si `katas-mcp-server-configuration` debe activarse y que agentes participan.

## Activation Check

- La tarea toca `.mcp.json` o `~/.claude.json`, scope de un server MCP, o credenciales de un server externo.
- Hay una decision de scope equipo vs personal que resolver.
- Hay un secreto filtrado en config versionada que remediar.
- No alcanza con un built-in (Grep/Read/Glob): si alcanza, NO activar y preferir el built-in.

## No activar cuando

- La peticion no menciona MCP, `.mcp.json`, scope ni credenciales de server.
- El input esta vacio o pide explicitamente saltar validacion y evidencia.
