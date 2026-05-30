<!--
generated-by: scripts/scaffold-skill.py
generated-for: hook-engineering
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Hook Engineering Deep Variation

Usar cuando el enforcement es de alto impacto o cruza varias tools (limites monetarios +
paths + modo plan/write, con normalizacion de outputs heterogeneos).

Incluir:

- Notas de descubrimiento: que limites son criticos y por que no pueden vivir en el prompt.
- Opciones consideradas: `matcher="*"` global vs por-tool; deny duro vs `ask`.
- Diseno del PreToolUse (inspeccion pura) y del PostToolUse (contrato unico de salida).
- Estrategia de hot-reload de la politica y manejo de JSON corrupto.
- Validacion contra la checklist completa y traza de auditoria por decision deny.
- Riesgos residuales (huecos de cobertura, handlers nuevos sin normalizar).
