<!--
generated-by: scripts/scaffold-skill.py
generated-for: agentic-loop-engineering
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Agentic Loop Engineering Deep Variation

Úsalo cuando el loop tiene consecuencias cruzadas: herramientas en paralelo, budget por tokens, transporte degradado, reintentos o compactación de contexto.

Incluye:

- Notas de descubrimiento: enumeración exhaustiva de los `stop_reason` del proveedor y qué handler recibe cada uno.
- Opciones consideradas: techo por iteraciones vs. por tokens; fallo fuerte vs. reintento acotado; serial vs. paralelo en el dispatch.
- Enfoque seleccionado con justificación (por qué el control vive en `stop_reason` y no en prosa).
- Loop construido en código (EN) con instrumentación de cada transición.
- Validación contra el checklist de `SKILL.md` y riesgos residuales (señales emergentes del SDK, `Transport closed`, fugas de gasto).
