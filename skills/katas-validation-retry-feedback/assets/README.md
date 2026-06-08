# Assets — katas-validation-retry-feedback

Estos assets definen el contrato determinístico para certificar reportes de retry con feedback de error.

- `validation-retry-contract.json`: campos requeridos y decisiones Guardian permitidas.
- `error-classification-policy.json`: taxonomía de errores recuperables y no recuperables.
- `feedback-specificity-policy.json`: requisitos mínimos para que un feedback sea específico.
- `retry-limit-policy.json`: cap de 2-3 intentos y reglas de escalada.
- `evidence-policy.json`: evidencia mínima para validar fuente, error y output previo.

Los assets son usados por `scripts/validate_validation_retry_feedback.py`, `scripts/check.sh`, `evals/evals.json` y los ejemplos de la skill.
