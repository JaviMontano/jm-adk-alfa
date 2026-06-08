# Example Output — Kata 26

## Summary

Dos errores con tratamiento distinto: `effective_date` es recuperable por formato y `total_amount` es no recuperable porque el dato no existe en la fuente. Se reintenta sólo el campo recuperable con feedback específico; el monto se escala a humano en lugar de inventarse.

## JSON Report

```json
{
  "schema": 1,
  "skill": "katas-validation-retry-feedback",
  "report_id": "contract-042-validation-retry",
  "scenario": "ContractFields extraction for contract-042.pdf",
  "source": "contract-042.pdf text excerpt says January 15, 2026 and contains no total amount clause",
  "schema_under_validation": "ContractFields(party_name: str, effective_date: date, total_amount: Decimal | null)",
  "evidence": [
    {
      "type": "source_excerpt",
      "detail": "Source includes January 15, 2026."
    },
    {
      "type": "validator_error",
      "detail": "effective_date invalid date format; total_amount is not a valid Decimal."
    },
    {
      "type": "absence_check",
      "detail": "Analyst notes confirm no total amount appears in the source."
    }
  ],
  "attempts": [
    {
      "attempt": 1,
      "status": "failed",
      "output": {
        "party_name": "Acme Corp",
        "effective_date": "01-15-2026",
        "total_amount": "no disponible"
      },
      "validator_error": {
        "error_type": "format_error",
        "path": "effective_date",
        "expected": "ISO 8601 date YYYY-MM-DD",
        "actual": "01-15-2026"
      },
      "feedback": {
        "message": "Path effective_date failed format_error: expected ISO 8601 date YYYY-MM-DD, actual 01-15-2026. Correct only effective_date using source text January 15, 2026.",
        "path": "effective_date",
        "expected": "ISO 8601 date YYYY-MM-DD",
        "previous_value": "01-15-2026",
        "scope_paths": ["effective_date"],
        "allowed_retry": true
      }
    },
    {
      "attempt": 2,
      "status": "valid",
      "output": {
        "party_name": "Acme Corp",
        "effective_date": "2026-01-15",
        "total_amount": null
      }
    }
  ],
  "classification": {
    "recoverability": "mixed",
    "recoverable_errors": ["format_error"],
    "nonrecoverable_errors": ["source_absent"],
    "retry_allowed": true,
    "escalation_required": true,
    "reason": "Only effective_date can be corrected from source evidence; total_amount is absent."
  },
  "outcome": {
    "final_status": "escalated",
    "retry_count": 1,
    "max_attempts": 2,
    "needs_human_review": true,
    "error_chain": [
      "effective_date: invalid date format, corrected on attempt 2",
      "total_amount: source_absent, escalated without retry"
    ],
    "structural_fix_required": false
  },
  "validation": {
    "generic_feedback_count": 0,
    "retry_count_with_specific_feedback": 1,
    "retry_count_exceeds_cap": false,
    "nonrecoverable_retried": false,
    "exhausted_attempts_escalated": false,
    "invalid_output_accepted": false,
    "deterministic_script_passed": true
  },
  "guardian": {
    "decision": "pass",
    "reason": "Recoverable date was retried with specific validator feedback; absent amount was escalated without invention."
  }
}
```

## Anti-patrón (ANTI)

```python
for _ in range(5):
    ext = extract(doc)        # mismo prompt, sin feedback
    try:
        return validate(ext)  # eventualmente "Decimal('0.00')" inventado
    except Exception:
        continue
```

Cinco reintentos ciegos terminan fabricando un `total_amount` para satisfacer el schema y aceptándolo en silencio: contrato downstream contaminado con un dato alucinado.

## Validation

- El retry inyectó el error de validación específico, con path, expectativa y valor previo.
- El cap de 2 intentos se respetó.
- El dato ausente en la fuente no se inventó: se marcó `needs_human_review`.
