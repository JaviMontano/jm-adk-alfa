# xlsx-template-creator scripts

## compile-xlsx-template.py

Validates a structured workbook template JSON and renders a deterministic Markdown report or YAML-like XLSX specification.

```bash
python3 skills/xlsx-template-creator/scripts/compile-xlsx-template.py \
  --input skills/xlsx-template-creator/scripts/fixtures/tracking-matrix.json \
  --format markdown
```

The script is read-only. It produces a specification for a renderer; it does not create a binary `.xlsx` file.
