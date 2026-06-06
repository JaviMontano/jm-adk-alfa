# Example Input — AI Assisted Testing

Generate an AI-assisted testing plan for `src/payments/validate_payment.py`.

Evidence:

- Requirements say amount must be positive, currency must be ISO-4217, and duplicate transaction IDs must be rejected.
- Existing tests cover valid card payments but not invalid currency, negative amount, duplicate transaction ID, or malformed JSON.
- Current coverage export shows branch coverage `68%`; target is `85%`.

Include unit tests, property tests, bounded fuzzing, and mutation testing. Do not claim execution results because tests have not been run.
