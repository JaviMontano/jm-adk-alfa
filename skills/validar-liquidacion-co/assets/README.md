# Validar Liquidacion Co Assets

These assets define the deterministic contract for validating Colombian labor settlement arithmetic offline. They are used by `SKILL.md`, `templates/output.md`, and `scripts/liquidacion_validator.py`.

## Asset Inventory

- `manifest.json`: declares every deterministic asset and where it is used.
- `output-contract.json`: required JSON report shape.
- `formula-policy.json`: arithmetic formulas used for recomputation.
- `tolerance-policy.json`: COP rounding and tolerance rules.
- `evidence-policy.json`: allowed evidence records and required fields.
- `paz-y-salvo-policy.json`: allowed arithmetic-only recommendation states.
- `legal-boundary-policy.json`: forbidden legal-final and signature-safety claims.

## Determinism Rules

- Use supplied inputs only.
- Use COP amounts only.
- Round calculated pesos with `ROUND_HALF_UP`.
- Accept component and net deltas only within COP 1.
- Treat the report as arithmetic validation, not legal advice.
- Block claims that a settlement is legally final, fully compliant, or safe to sign.
