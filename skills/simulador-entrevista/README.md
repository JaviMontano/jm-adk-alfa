# simulador-entrevista

Deterministic mock-interview practice. The skill asks or evaluates one question per turn and keeps feedback separate across substance, English, and presence. Reports are validated offline and cannot use overall averages or guaranteed-success language.

## Offline Validation

```bash
bash skills/simulador-entrevista/scripts/check.sh
python3 -B scripts/validate-skill-dod.py --skill simulador-entrevista
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill simulador-entrevista
```

## Determinism Rules

- Use one-question mode.
- Keep `substance`, `english`, and `presence` separate.
- Require score evidence snippets.
- Select one next step from the weakest dimension.
- Block averages, success guarantees, fabricated stories, and unsupported languages.
