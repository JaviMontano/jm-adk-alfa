<!--
generated-by: scripts/scaffold-skill.py
generated-for: few-shot-engineering
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Example Input

Tengo un clasificador de tickets de soporte que devuelve JSON:
`{"category": "billing|technical|spam", "priority": "low|high"}`.

Acierta en los tickets obvios, pero falla en los grises:

- "No me llegó la factura pero tampoco la necesito ya" -> lo manda a `technical`.
- "URGENTE!!! gané un premio, click aquí http://..." -> lo marca `high`.
- "El servidor responde 500 a veces, no siempre" -> lo marca `low`.

Diseña un bloque few-shot que calibre estos bordes sin romper el prefix cache.
