# Scripts

## liquidacion_validator.py

Validates deterministic Colombian liquidation arithmetic reports. It checks evidence, currency, formulas, tolerance, component deltas, net reconciliation, paz y salvo posture, and legal-boundary flags.

```bash
python3 skills/validar-liquidacion-co/scripts/liquidacion_validator.py --input skills/validar-liquidacion-co/scripts/fixtures/valid-clean-arithmetic.json
```

## check.sh

Runs valid, blocked, and invalid fixtures offline. Expected result: valid fixtures exit `0`; blocked and invalid fixtures exit non-zero.
