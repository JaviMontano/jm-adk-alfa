<!--
generated-by: scripts/scaffold-skill.py
generated-for: mcp-engineering
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Mcp Engineering

Configurar MCP servers (project vs user scope, env-var expansion) y disenar contratos de error tipados con categoria y retryable.

## Triggers

- mcp engineering
- mcp server config
- mcp error contract
- mcp scope

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Resumen ejecutivo

Capacidad de ingeniería para integrar servidores MCP en producción: scope correcto (project vs user), credenciales por expansión de variables de entorno y contratos de error tipados (`isError`, `errorCategory`, `isRetryable`, `retryAfterSeconds`) con la política de reintento en el cliente, no en el modelo.

## Quick Use

Invócala cuando configures un servidor MCP para un equipo, cuando un servidor devuelva errores que el modelo reintenta a ciegas, o cuando debas decidir MCP frente a un tool built-in. Entrega: bloque `.mcp.json` versionable + contrato de error tipado + checklist de validación.

## Output Format

Markdown con summary, evidence, result, validation y risks. Config en bloques de código (`.mcp.json`, contrato de error en TS/JSON).
