# Form UX Advanced Scripts

## `audit-form-ux.py`

Audits a structured form journey and emits a deterministic Markdown scorecard.

```bash
python3 skills/form-ux-advanced/scripts/audit-form-ux.py \
  --journey skills/form-ux-advanced/scripts/fixtures/intake-journey.json
```

The script writes only when `--output` is provided. Invalid journey specs fail nonzero.
