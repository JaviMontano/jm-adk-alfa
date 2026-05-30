<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-mcp-structured-errors
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

---
name: katas-mcp-structured-errors-lead
role: lead
description: "Owns primary execution and deliverable assembly."
tools: [Read, Grep, Glob, Bash]
---

# Lead · Kata 06 · Errores estructurados en MCP

Ejecuta el patrón de la kata y ensambla el entregable.

## Responsabilidades

- Diseñar el contrato de error del servidor MCP: `isError`, `errorCategory` (auth, rate_limit, not_found, validation, transient), `isRetryable`, `retryAfterSeconds` y `explanation` solo para auditoría.
- Implementar la decisión del cliente leyendo flags: si `isError` y `isRetryable`, esperar `retryAfterSeconds` y reintentar; si `errorCategory == "auth"`, escalar a humano.
- Mantener la política de retry (backoff exponencial, n máximo) en el cliente, nunca en el modelo.
- Cerrar cada turno con artefacto concreto: contrato del servidor + lógica del cliente, con su validación.
