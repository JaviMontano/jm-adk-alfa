<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-headless-code-review
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Headless Code Review Deep Variation

Usar cuando hay que diseñar el pipeline desde cero o auditar uno existente sospechoso de parsear prosa.

Incluye:

- Diseño del schema de anotaciones (`annotations.schema.json`): campos `required`, enum de `severity`, alineado con extracción defensiva (Kata 5).
- Workflow completo de CI con `claude -p ... --output-format=json --schema ...` y step de validación `post_annotations.py`.
- Lógica de fallo del job ante JSON inválido (control por señal, Kata 1) y manejo de `out.json` ausente/vacío.
- Auditoría del anti-patrón: localizar cualquier `grep`/`awk`/regex sobre la salida del modelo y reemplazarlo por validación de schema.
- Justificación del gate humano de merge (FP/FN, responsabilidad legal) y riesgos residuales (rate limits, reintentos a nivel pipeline).
