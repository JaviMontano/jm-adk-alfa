# Cierre Conversacion Scripts

This directory contains deterministic offline validation for JSON closeout reports.

## Contract

- `check.sh` runs with no network, no wall-clock dependency, and no random input.
- Valid fixtures must pass.
- Invalid fixtures must fail.
- Scripts are read-only and do not write durable logs.

## Validate

```bash
bash skills/cierre-conversacion/scripts/check.sh
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill cierre-conversacion
```
