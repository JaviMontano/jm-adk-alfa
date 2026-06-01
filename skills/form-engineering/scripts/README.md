# Form Engineering Scripts

## `compile-form-contract.py`

Compiles a structured JSON form spec into a deterministic Markdown implementation contract.

```bash
python3 skills/form-engineering/scripts/compile-form-contract.py \
  --spec skills/form-engineering/scripts/fixtures/enterprise-intake-spec.json
```

The script writes only when `--output` is provided. Invalid specs fail nonzero.
