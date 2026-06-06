# Brand XLSX Example Output

## Summary

- Generated `AtlasOps KPI Workbook.xlsx` as a real XLSX package. [CÓDIGO]
- Applied supplied brand colors, sheet name, title, year, and domain. [CÓDIGO]
- Rejected remote assets, unresolved placeholders, and renamed HTML/CSV output.
  [CONFIG]

## Artifact

- Path: `AtlasOps KPI Workbook.xlsx` [CÓDIGO]
- Format: Microsoft Excel XLSX ZIP package [CÓDIGO]
- Core title: `AtlasOps KPI Workbook` [CÓDIGO]
- Creator: `brand-xlsx` [CÓDIGO]
- Artifact date: `2026-06-06` [CÓDIGO]

## Validation

- Required ZIP parts exist: `[Content_Types].xml`, `_rels/.rels`,
  `docProps/core.xml`, `xl/workbook.xml`, `xl/_rels/workbook.xml.rels`,
  `xl/styles.xml`, `xl/worksheets/sheet1.xml`. [CÓDIGO]
- Brand tokens present: `#2563EB`, `#0F172A`, `#FFFFFF`, `#F8FAFC`,
  `#475569`, `#EFF6FF`, `Calibri`. [CÓDIGO]
- Workbook features include meaningful sheet name, primary tab color, merged
  title/footer, freeze panes, auto filter, bounded column widths, and footer
  metadata. [CÓDIGO]
- `bash skills/brand-xlsx/scripts/check.sh` passes. [CÓDIGO]

## Risks And Limits

- Installed font availability can affect visual rendering in Excel; fallback
  font remains declared. [INFERENCIA]
