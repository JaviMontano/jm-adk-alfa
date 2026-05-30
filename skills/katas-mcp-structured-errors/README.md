<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-mcp-structured-errors
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Kata 06 · Errores estructurados en MCP

Un servidor MCP que falla devuelve un payload tipado (`isError`, `errorCategory`, `isRetryable`, `retryAfterSeconds`). El agente decide retry, escalada o aborto leyendo los flags, no la prosa del error. La política de retry (backoff exponencial, n máximo) vive en el cliente, no en el modelo. `explanation` es para el humano que audita el log.

Evita el anti-patrón del string genérico `"something went wrong"`, que obliga al modelo a adivinar y produce reintentos infinitos, abandono prematuro o escaladas innecesarias.

## Triggers

- mcp structured error
- error category
- retryable error
- typed error contract

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

Activa esta skill cuando diseñes o audites el contrato de error de un tool/servidor MCP, o cuando un agente reintente sin fin, abandone o escale por leer prosa en lugar de flags tipados.

## Output Format

Markdown con summary, evidence, result, validation y risks. El result distingue contrato del servidor (flags) de política del cliente (retry).
