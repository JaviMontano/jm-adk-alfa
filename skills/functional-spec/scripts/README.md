# Functional Spec Scripts

## `compile-functional-spec.py`

Compiles a structured JSON specification into a deterministic Markdown functional spec.

```bash
python3 skills/functional-spec/scripts/compile-functional-spec.py \
  --spec skills/functional-spec/scripts/fixtures/mvp-spec.json
```

The script writes only when `--output` is provided. Invalid specs fail nonzero.
