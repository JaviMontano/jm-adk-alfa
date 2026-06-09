---
name: validar-liquidacion-co
version: 0.2.0
description: "This skill should be used when the user asks to validate a Colombian labor settlement calculation, recompute cesantias, intereses de cesantias, prima, vacaciones, deductions, net payment, or review paz y salvo questions with an arithmetic-only, evidence-backed report."
owner: "JM Labs"
triggers:
  - validar-liquidacion
  - liquidacion-co
  - finiquito
  - Colombian labor settlement
  - paz y salvo
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# Validar Liquidacion Co

## Purpose

Validate arithmetic in a Colombian labor settlement packet using supplied data only. Recompute cesantias, intereses de cesantias, prima, vacaciones, deductions, and net amount; list deviations and open questions; and mark paz y salvo posture as arithmetic-only.

This skill does not provide legal advice. It must recommend legal/accounting review for final decisions, especially when contract type, salary factors, indemnity, sanctions, collective agreements, or disputed facts are involved.

## Deterministic Contract

Follow `assets/output-contract.json` and validate reports with `scripts/liquidacion_validator.py`. A valid report must include:

- Currency `COP`.
- Evidence records for input values and source documents.
- `calculation_basis` with salary bases, days worked, and vacation basis.
- Reported components and deductions.
- Recomputed components using `assets/formula-policy.json`.
- Tolerance from `assets/tolerance-policy.json`.
- `paz_y_salvo` posture from `assets/paz-y-salvo-policy.json`.
- Validation flags: `offline=true`, `network_used=false`, `not_legal_advice=true`, `legal_review_recommended=true`.

## Formula Policy

Use deterministic formulas for arithmetic checking only:

- `cesantias = salary_base_prestaciones * days_worked / 360`
- `intereses_cesantias = cesantias * 0.12 * days_worked / 360`
- `prima = salary_base_prestaciones * days_worked / 360`
- `vacaciones = salary_base_vacaciones * vacation_days / 30` when vacation days are supplied
- otherwise `vacaciones = salary_base_vacaciones * days_worked / 720`

Do not infer salary factors, contract type, transport allowance treatment, indemnity, sanctions, or deductions that are not supplied.

## Workflow

1. Inventory supplied documents and assign evidence IDs such as `E-001`.
2. Extract numeric inputs exactly as supplied: salary bases, days, vacation days, reported components, deductions, and reported net.
3. Validate all amounts are COP and non-negative.
4. Recompute components with the formula policy and tolerance.
5. Compare reported component amounts and net amount.
6. Create open questions for missing basis, unclear deductions, disputed vacation days, or paz y salvo uncertainty.
7. Use `sign_under_reservation` or `do_not_sign_yet` when questions remain.
8. Validate the JSON report with `scripts/liquidacion_validator.py`.

## Output Rules

- Tag claims with `[EXPLICIT]`, `[INFERRED]`, or `[OPEN]`.
- State arithmetic result separately from legal conclusion.
- Never say a settlement is legally final, safe to sign, or fully compliant.
- Never use web, payroll systems, or current legal tables unless the user supplies them as evidence.
- Never touch or depend on `firma-pdf-legal`; signature automation remains out of scope.

## Assets

- `assets/manifest.json` lists deterministic assets.
- `assets/output-contract.json` defines the report shape.
- `assets/formula-policy.json` defines formulas used by the offline validator.
- `assets/tolerance-policy.json` defines COP rounding tolerance.
- `assets/evidence-policy.json` defines allowed evidence and required fields.
- `assets/paz-y-salvo-policy.json` defines safe recommendations when questions remain.
- `assets/legal-boundary-policy.json` defines no-legal-advice blockers.

## Scripts

Run:

```bash
python3 skills/validar-liquidacion-co/scripts/liquidacion_validator.py --input <report.json>
bash skills/validar-liquidacion-co/scripts/check.sh
```

The validator is offline and rejects missing evidence, non-COP currency, negative amounts, component deviations beyond tolerance, net mismatches, unsafe paz y salvo posture, network use, and legal-final language.

## Related Skills

- `negociacion-oferta`
- `proceso-seleccion-orchestrator`

## Stop Conditions

Stop when the user asks for legal certainty, signature automation, litigation advice, payroll-system access, or a final compliance opinion without professional review.
