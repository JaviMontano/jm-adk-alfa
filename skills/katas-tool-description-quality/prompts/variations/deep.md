<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-tool-description-quality
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Tool Description Quality Deep Variation

Úsala cuando la toolset es grande, hay overloading que exige split, o el system prompt sesga el routing.

Incluye: notas de descubrimiento (qué pares solapan y por qué), opciones consideradas por tool (rename vs split vs solo frontera), el split propuesto (un tool multimodo → varios de propósito único con input_schema distintos), las keywords del system prompt detectadas y cómo se neutralizan en la descripción, la validación (misroute esperado tras el cambio) y los riesgos.
