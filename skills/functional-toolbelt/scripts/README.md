# Functional Toolbelt Scripts

## `compile-functional-toolbelt.py`

Validates a structured six-tool functional analysis input and emits a deterministic Markdown report.

```bash
python3 skills/functional-toolbelt/scripts/compile-functional-toolbelt.py \
  --input skills/functional-toolbelt/scripts/fixtures/toolbelt-input.json
```

The script writes only when `--output` is provided. Invalid or incomplete toolbelt inputs fail nonzero.
