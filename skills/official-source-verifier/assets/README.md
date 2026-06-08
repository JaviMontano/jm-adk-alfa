# Assets — official-source-verifier

Estos assets definen el contrato determinístico para certificar paquetes de verificación contra fuentes oficiales.

- `official-source-verifier-contract.json`: campos requeridos del reporte.
- `source-priority-policy.json`: jerarquía y roles permitidos por tipo de fuente.
- `claim-evidence-policy.json`: requisitos de evidencia por claim.
- `citation-policy.json`: URL, publisher y fecha de consulta.
- `decision-policy.json`: reglas para autorizar o bloquear cambios.
- `evidence-policy.json`: evidencia mínima aceptada.

Los assets son usados por `scripts/validate_official_source_verifier.py`, `scripts/check.sh`, `evals/evals.json` y ejemplos.
