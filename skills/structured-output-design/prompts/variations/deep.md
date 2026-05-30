<!--
generated-by: scripts/scaffold-skill.py
generated-for: structured-output-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Structured Output Design Deep Variation

Úsala cuando la fuente es heterogénea, el dataset aguas abajo es crítico o el schema impacta varios consumidores.

Incluye:

1. **Inventario con evidencia.** Para cada campo, en qué fracción de los documentos de muestra aparece; eso decide `required` vs `nullable`.
2. **Opciones de modelado.** Por campo dudoso: unión nullable vs default vs omitir; por categórico: enum cerrado vs enum+`'other'` vs string libre. Justifica la elegida.
3. **Decisión de `tool_choice`.** Forzar vs `auto` vs `any`, según si hay otras tools (extraer vs escalar, por ejemplo).
4. **Validación y recuperación.** Cómo se valida la salida contra el schema y cómo se conecta a `validation-retry-design`/`self-correction-loops` cuando falla.
5. **Provenance si aplica.** Si cada campo necesita su fuente, conecta con `provenance-engineering`.
6. **Riesgos residuales.** Campos que aún pueden romper, casos de la cola larga, evolución prevista del enum.

Cierra con el schema final, el patrón GOOD/ANTI y el checklist completo.
