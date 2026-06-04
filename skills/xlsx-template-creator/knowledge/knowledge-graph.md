# XLSX Template Creator -- Knowledge Graph

## Core Concepts

- `xlsx-template-creator`: creates renderer-ready workbook specifications.
- `workbook-spec`: JSON source contract for the compiler.
- `template-policy`: required sheets, semantic colors, and formatting minimums.
- `formula-policy`: guarded formulas, blocked volatile functions, dropdown sources, and named range patterns.
- `compiler`: deterministic validation and Markdown/YAML renderer.
- `renderer-handoff`: final artifact passed to an XLSX renderer.

## Flow

`User workbook request` -> `workbook-spec` -> `compile-xlsx-template.py` -> `validated report` -> `XLSX renderer handoff`
