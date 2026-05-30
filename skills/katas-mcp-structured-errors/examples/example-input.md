<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-mcp-structured-errors
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Input · Kata 06 · Errores estructurados en MCP

Escenario: API Integration Reliability. Nuestro servidor MCP `crm_lookup` consulta una API externa con rate limit. Hoy el handler hace:

```python
except Exception as e:
    return {"error": f"failed: {e}"}
```

El agente, al ver el string, a veces reintenta para siempre y otras veces escala a un humano un simple rate limit. Necesito convertir el contrato de error en algo tipado y mover la política de retry al cliente. Las excepciones posibles son `RateLimitException` (trae `retry_after`), `AuthException`, `NotFoundException` y errores transitorios de red.
