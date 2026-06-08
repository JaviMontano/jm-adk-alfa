# Kata 26 · Variante rápida — Validación y Retry con Error Feedback

Úsala cuando el error es claramente recuperable (formato) y el schema es simple.

- Reintenta con path, expected, previous value y error específico; máximo 2 intentos totales.
- Si valida, devuelve la extracción con `attempts`.
- Si no valida en el cap, marca `needs_human_review` con `error_chain`.
- Si aparece un error no recuperable durante la revisión, no lo reintentes.

Devuelve solo el deliverable, el estado de validación y los riesgos residuales.
