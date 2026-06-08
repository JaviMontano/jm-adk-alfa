# Kata 26 · Variante profunda — Validación y Retry con Error Feedback

Úsala cuando hay que decidir si un error es recuperable o no recuperable, cuando aparecen patrones sistemáticos, o cuando el contrato downstream es de alto impacto.

- Analiza si el dato existe en la fuente antes de reintentar (no recuperable → escalar, no inventar).
- Mide la distribución de errores: si el mismo error domina, recomienda fix estructural (schema/prompt/post-process) en lugar de subir retries.
- Diseña el registro de escalada (`needs_human_review`, `error_chain`, `attempts`) que consumirá el revisor humano.
- Produce o revisa un reporte JSON compatible con `assets/validation-retry-contract.json`.
- Verifica con `scripts/check.sh` cuando haya fixtures o reporte local que auditar.

Incluye notas de discovery, opciones consideradas, enfoque elegido, validación y riesgos.
