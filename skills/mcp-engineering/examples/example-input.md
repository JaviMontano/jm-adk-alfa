# Example Input

> Necesito integrar nuestro servidor MCP de facturación (`billing`) para todo el equipo. Usa la API key `BILLING_API_KEY`. El servidor a veces devuelve 429 (rate limit) y a veces 500 transitorios; hoy el modelo reintenta cualquier error a ciegas. Quiero la config versionada y un contrato de error que el cliente pueda leer para decidir el reintento.

Produce un reporte JSON compatible con `assets/mcp-engineering-contract.json`, incluyendo scope, config, credenciales por env-var, contrato de error, retry policy, revisión built-in, evidencia y decisión Guardian.
