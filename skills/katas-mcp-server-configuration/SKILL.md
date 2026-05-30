---
name: katas-mcp-server-configuration
version: 1.0.0
description: "Configuracion de MCP servers: project vs user scope, env-var expansion para credenciales y rotacion ante secreto leakeado."
owner: "JM Labs"
triggers:
  - mcp server configuration
  - mcp scope
  - env var credentials
  - mcp json config
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Kata 22 · Configuracion de MCP Servers

## Que es

Los MCP servers se declaran en `.mcp.json` (project scope, versionado con el repo) o en `~/.claude.json` (user scope, personal). Las credenciales se inyectan mediante env-var expansion (`${GITHUB_TOKEN}`), nunca hardcodeadas. Al conectarse, Claude Code descubre simultaneamente todos los servers declarados y expone sus tools y resources.

La decision central es de scope: un server en `.mcp.json` viaja con el repositorio y sirve a toda la flota; un server en `~/.claude.json` solo existe en tu laptop. La eleccion equivocada deja a la mitad del equipo sin acceso, o publica un secreto.

## Por que importa (falla que evita)

- Hardcodear un token en `.mcp.json` versionado equivale a publicarlo: queda en el historial de git para siempre.
- Poner reglas de equipo en `~/.claude.json` deja a los nuevos devs sin acceso al server: la config no se replica.
- Activar un MCP cuando un built-in (Grep, Read, Glob) ya cubre el caso es overkill que infla la superficie de tools sin ganancia.
- Ante un secreto leakeado, agregar el archivo a `.gitignore` NO lo remueve: ya esta versionado.

## Modelo mental

- Project scope (`.mcp.json`): viaja con el repo, descubrimiento automatico al conectar, sirve a toda la flota.
- User scope (`~/.claude.json`): experimentos personales que no afectan al equipo.
- Credenciales siempre por `${ENV_VAR}` expansion, nunca literal en el archivo.
- MCP resources (catalogos) reducen llamadas exploratorias frente a invocar tools una y otra vez.
- MCP solo cuando un built-in no aplica: la integracion externa se justifica, no se asume.

## Patron correcto

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_TOKEN": "${GITHUB_TOKEN}" }
    },
    "internal-docs": {
      "command": "node",
      "args": ["./scripts/mcp-docs.js"]
    }
  }
}
```

Server de equipo en `.mcp.json` versionado, credencial inyectada por env-var expansion (`${GITHUB_TOKEN}`), server interno sin secreto apuntando a un script del repo.

## Anti-patron

```json
{ "env": { "GITHUB_TOKEN": "ghp_AbCdEfG123456789" } }
```

Token literal hardcodeado en un archivo versionado. Queda expuesto en el historial de git; agregar el archivo a `.gitignore` no lo remueve.

## Argumento de certificacion

Para certificar dominio de esta kata el agente debe:

- Distinguir project vs user scope con criterio (config de equipo va a `.mcp.json` versionado).
- Defender env-var expansion para credenciales en lugar de literales.
- Justificar un MCP solo cuando un built-in no aplica (Grep cubre busqueda en filesystem local; MCP seria overkill).
- Responder a un secreto leakeado con rotacion de la credencial + reemplazo por `${ENV}` + purga del historial (git filter-repo), no con `.gitignore`.

## Cuando activar

- Configurar o revisar `.mcp.json` o `~/.claude.json`.
- Decidir el scope de un server MCP (equipo vs personal).
- Manejar credenciales de un server externo.
- Responder a un token o secreto filtrado en config versionada.

## Skills relacionadas

- `katas-builtin-tool-selection`
- `katas-custom-commands-skills`
- `katas-hierarchical-claude-memory`
