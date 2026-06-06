# Brand XLSX

Deterministic branded Microsoft Excel generation for `.xlsx` artifacts with
real package validation, brand tokens, core properties, workbook styles, freeze
panes, merged title/footer regions, and footer metadata. [CONFIG]

## Triggers

- "generate a branded spreadsheet"
- "create an Excel file with brand colors"
- "build an XLSX report"
- "apply brand styling to a spreadsheet"
- "create a KPI dashboard in Excel"
- "use openpyxl"

## Assets

- `assets/activation-policy.json`: activation and routing rules.
- `assets/brand-xlsx-contract.json`: XLSX workbook contract and validator
  checks.
- `assets/fallback-brand-config.json`: deterministic fallback brand tokens.
- `assets/style-token-map.json`: token-to-workbook-style mapping.
- `assets/evidence-policy.json`: evidence tag and validation report policy.

## Scripts

Run deterministic fixtures:

```bash
bash skills/brand-xlsx/scripts/check.sh
```

The check validates accepted XLSX packages and rejects HTML/CSV renamed as
XLSX, missing workbook parts, remote assets, unresolved placeholders, and
legacy hardcoded colors. [CÓDIGO]

## Output

Return a saved `.xlsx` path plus validation evidence, or instructions only when
the user asks for a plan. Do not return CSV, HTML, or Markdown as XLSX.
