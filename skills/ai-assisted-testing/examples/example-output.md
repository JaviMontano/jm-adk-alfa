# Example Output — AI Assisted Testing

## Summary

The highest-value additions are negative amount, invalid currency, duplicate transaction ID, malformed JSON, and branch-oriented property tests for `validate_payment.py`. [DOC]

## Candidate Tests

| id | type | target | oracle | status |
|----|------|--------|--------|--------|
| T-001 | unit | `validate_payment.amount` | rejects `amount <= 0` with validation error | proposed |
| T-002 | unit | `validate_payment.currency` | rejects non ISO-4217 currency code | proposed |
| T-003 | regression | `validate_payment.transaction_id` | rejects duplicate transaction ID | proposed |
| T-004 | fuzz | JSON request parser | malformed payload never bypasses validation | proposed |

## Coverage Plan

- Current branch coverage: `68%`. [MÉTRICA]
- Target branch coverage: `85%`. [CONFIG]
- Target module: `src/payments/validate_payment.py`. [CÓDIGO]

## Fuzzing Bounds

- Domain: payment JSON payloads with amount, currency, transaction ID, and optional metadata. [CONFIG]
- Seed policy: deterministic seed list from valid and invalid examples. [CONFIG]
- Iterations: `500`. [CONFIG]
- Timeout: `2s` per generated case. [CONFIG]
- Safety: local parser only; no production endpoint. [CONFIG]

## Validation

- Tests are proposed, not executed. [CONFIG]
- Every test includes target, rationale, oracle, and evidence mapping. [CÓDIGO]
