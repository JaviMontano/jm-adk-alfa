<!--
generated-by: scripts/scaffold-skill.py
generated-for: negociacion-oferta
generated-on: 2026-06-05
overwrite-policy: missing-only unless --force
-->

# Negociacion Oferta Scripts

This directory contains deterministic local automation for `negociacion-oferta`.

## Contract

- Scripts are non-destructive by default.
- Runtime checks live in `check.sh`.
- Fixtures in `fixtures/` are stable and valid JSON.
- Any script that mutates files must require an explicit apply flag.

## Validate

```bash
python3 scripts/validate-skill-scripts.py --strict --run-checks
```
