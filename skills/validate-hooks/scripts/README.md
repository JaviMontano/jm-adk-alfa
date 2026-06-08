# Scripts for validate-hooks

[CODE] `compile-validate-hooks.py` validates `hooks.json` structure and renders a deterministic offline audit report.

## Commands

```bash
python3 skills/validate-hooks/scripts/compile-validate-hooks.py \
  --input skills/validate-hooks/scripts/fixtures/valid-hooks-audit-input.json

python3 skills/validate-hooks/scripts/compile-validate-hooks.py \
  --hooks-json hooks/hooks.json \
  --plugin-root .

bash skills/validate-hooks/scripts/check.sh
```

[CODE] The compiler reads hook configuration, script paths, and local assets only. It never executes hook commands.
