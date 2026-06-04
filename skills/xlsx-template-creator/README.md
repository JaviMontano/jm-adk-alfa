# XLSX Template Creator

`xlsx-template-creator` produces auditable workbook specifications for XLSX renderers. It defines the workbook contract first, validates the contract with local scripts, and returns Markdown or YAML-like output that can be reviewed before a binary file is generated.

## Inputs

- Template type: `tracking-matrix` or `metrics-dashboard`.
- Workbook title and locale.
- Required columns, dropdown values, formulas, KPI names, targets, and thresholds.
- Renderer name and output constraints.

## Outputs

- Sheet inventory with required workbook tabs.
- Column contract with headers, widths, types, formulas, and data-validation sources.
- Named range table.
- Validation evidence.
- Handoff notes for a downstream XLSX renderer.

## Deterministic Script

```bash
python3 skills/xlsx-template-creator/scripts/compile-xlsx-template.py \
  --input skills/xlsx-template-creator/scripts/fixtures/tracking-matrix.json \
  --format markdown
```

Run `bash skills/xlsx-template-creator/scripts/check.sh` to validate assets, fixtures, compiler output fragments, and negative cases.
