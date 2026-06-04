# XLSX Template Creator -- Body of Knowledge

## Canon

This skill creates workbook specifications for spreadsheet renderers. It does not directly write binary XLSX files. The canonical artifact is a validated JSON-derived Markdown or YAML-like contract that a renderer can convert into a workbook.

## Core Objects

- Workbook spec: top-level object with `templateType`, `title`, `locale`, `sheets`, `namedRanges`, `validation`, and `handoff`.
- Sheet contract: `name`, `purpose`, `columns`, `printArea`, plus data-area controls.
- Column contract: `header`, `width`, `type`, `description`, and optional `source`, `formula`, or `conditionalFormat`.
- Named range: workbook-safe name mapped to a sheet cell range.
- Validation row: explicit check, status, and evidence that the spec is render-safe.
- Handoff: renderer name, output format, and notes for binary-only features.

## Deterministic Quality Signals

| Signal | Good State | Failure State |
|---|---|---|
| Required sheets | Tracking uses Tracker/Summary/Config; dashboard uses KPIs/Trends/Alerts/Config | Ad hoc sheets replace required tabs |
| Formulas | Start with `=` and guard division with `IF` | Unguarded ratios or volatile/external functions |
| Dropdowns | Source values from Config or named ranges | Dropdowns reference arbitrary external sheets |
| Formatting | Semantic colors and no merged cells in data areas | Decorative colors or merged sortable/filterable rows |
| Validation | Evidence rows document checks | Output trusts prose without machine validation |

## Limits

The compiler validates workbook structure, formula safety signals, dropdown sources, and report rendering. It does not open Excel, generate native charts, freeze panes, or prove compatibility with every renderer implementation.
