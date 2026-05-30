<!--
generated-by: scripts/scaffold-skill.py
generated-for: mcp-engineering
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Example Input

> Necesito integrar nuestro servidor MCP de facturación (`billing`) para todo el equipo. Usa la API key `BILLING_API_KEY`. El servidor a veces devuelve 429 (rate limit) y a veces 500 transitorios; hoy el modelo reintenta cualquier error a ciegas. Quiero la config versionada y un contrato de error que el cliente pueda leer para decidir el reintento.
