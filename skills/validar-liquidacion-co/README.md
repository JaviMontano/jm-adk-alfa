# validar-liquidacion-co

Deterministic arithmetic validator for Colombian labor settlement packets. It recomputes supplied components, compares reported values, checks net payment, and flags paz y salvo questions. It is arithmetic-only and always preserves the legal/accounting review boundary.

## Offline Validation

```bash
bash skills/validar-liquidacion-co/scripts/check.sh
python3 -B scripts/validate-skill-dod.py --skill validar-liquidacion-co
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill validar-liquidacion-co
```

## Determinism Rules

- Use supplied numbers only.
- Require COP currency and evidence IDs.
- Apply formula policy and COP tolerance deterministically.
- Separate arithmetic findings from legal conclusions.
- Block unsafe paz y salvo recommendations when questions remain.
