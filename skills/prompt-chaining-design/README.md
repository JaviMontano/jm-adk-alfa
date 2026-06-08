# Prompt Chaining Design

`prompt-chaining-design` decomposes large work into a typed local pass and an integration pass over summaries. The local pass processes exactly one unit at a time, emits a schema-validated summary, and records typed errors per unit. The integration pass consumes only summaries and must never reopen raw units as a shortcut.

## Deterministic Contract

The `assets/` directory defines:

- when chaining is justified over single-pass,
- atomic unit boundaries,
- local pass schema requirements,
- transition schema requirements,
- integration pass constraints,
- per-unit error handling,
- Guardian pass/block decisions.

## Local Validation

```bash
bash skills/prompt-chaining-design/scripts/check.sh
```

The check validates good chain design reports and rejects reports where the integration pass sees raw data, schemas are missing, local passes process multiple units, typed error propagation is absent, chaining is unjustified, or Guardian passes a blocked design.
