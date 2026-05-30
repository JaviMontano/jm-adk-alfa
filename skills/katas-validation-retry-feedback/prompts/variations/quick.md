<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-validation-retry-feedback
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Kata 26 · Variante rápida — Validación y Retry con Error Feedback

Úsala cuando el error es claramente recuperable (formato) y el schema es simple.

- Reintenta con el error específico, máximo 2 intentos.
- Si valida, devuelve la extracción con `attempts`.
- Si no, marca `needs_human_review` con el error.

Devuelve solo el deliverable, el estado de validación y los riesgos residuales.
