# Funnel Design Scripts

## compile-funnel-design.py

Compiles a structured funnel design JSON file into a deterministic Markdown report.

```bash
python3 skills/funnel-design/scripts/compile-funnel-design.py \
  --input skills/funnel-design/scripts/fixtures/funnel-design-input.json \
  --output /tmp/funnel-design.md
```

## check.sh

Validates fixtures, assets, report fragments, and invalid-input failure behavior.
