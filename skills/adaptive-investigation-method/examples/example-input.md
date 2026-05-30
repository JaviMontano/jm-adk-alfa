<!--
generated-by: scripts/scaffold-skill.py
generated-for: adaptive-investigation-method
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Example Input

Construye un agente que use `adaptive-investigation-method` para responder esta pregunta sobre un monorepo desconocido de ~4.000 archivos:

> "¿Donde se valida la autenticacion de las requests entrantes y que pasa si el token expira?"

Restricciones de ingenieria:

- Budget de exploracion: maximo 8 lecturas completas (`Read`).
- No leer el repo entero; el mapeo inicial debe ser barato.
- Re-planificar solo si una hipotesis queda invalidada por evidencia.
- Entregar la respuesta con referencia a archivo/linea, mas riesgos residuales.
