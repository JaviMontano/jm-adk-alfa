---
name: xlsx-template-creator
version: 1.0.0
description: "Generates deterministic XLSX template specifications for tracking matrices and metrics dashboards. Use when the user asks to create a spreadsheet template, build a tracking matrix, design a KPI dashboard, generate an XLSX spec, define workbook columns, or validate spreadsheet formulas and dropdown ranges before rendering."
argument-hint: "tracking-matrix|metrics-dashboard title"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
model: opus
context: fork
---

# XLSX Template Creator

Generate a renderer-ready workbook specification, not a binary `.xlsx` file. The output is a structured Markdown or YAML-like spec that defines sheets, columns, formulas, dropdowns, named ranges, validation evidence, and handoff notes for a downstream XLSX renderer.

## Deterministic Bundle

Use the local compiler whenever the user needs a repeatable template contract, validation before handoff, or a diffable workbook spec.

```bash
python3 scripts/compile-xlsx-template.py --input path/to/workbook-spec.json --format markdown
python3 scripts/compile-xlsx-template.py --input path/to/workbook-spec.json --format yaml --output workbook-template.yml
```

The compiler loads:

| File | Purpose |
|---|---|
| `assets/xlsx-template-schema.json` | Required workbook, sheet, column, named range, validation, and handoff fields. |
| `assets/template-policy.json` | Accepted template types, required sheets, semantic colors, and formatting minimums. |
| `assets/formula-policy.json` | Formula safety rules, dropdown source prefixes, blocked functions, and named range patterns. |
| `assets/report-template.md` | Stable Markdown report shape. |

Run `bash scripts/check.sh` after changing this skill, its assets, or fixtures.

## Workflow

1. Identify the template type: `tracking-matrix` for task/compliance/item tracking, or `metrics-dashboard` for KPI monitoring and thresholds.
2. Ask only for missing essentials: title, locale, workbook audience, required fields, dropdown values, KPI names, targets, thresholds, and renderer constraints.
3. Create a JSON workbook spec that follows `assets/xlsx-template-schema.json`.
4. Validate the spec with `scripts/compile-xlsx-template.py`; fix every error before returning the template.
5. Return the compiled Markdown for human review, or YAML when the next step is machine rendering.
6. Include handoff notes that name the intended renderer and any features that renderer must add natively, such as charts or sparklines.

## Template Types

| Signal | Choose | Required sheets |
|---|---|---|
| Tasks, owners, due dates, priorities, compliance rows, status tracking | `tracking-matrix` | `Tracker`, `Summary`, `Config` |
| KPIs, current vs target, trends, thresholds, alert queues | `metrics-dashboard` | `KPIs`, `Trends`, `Alerts`, `Config` |

If the user needs both, produce two specs and give them distinct titles.

## Workbook Rules

- Every sheet must declare `purpose`, `columns`, and `printArea`.
- Data sheets must enable `autoFilter` when they are `Tracker`, `KPIs`, or `Alerts`.
- Data areas must set `mergedCellsInDataArea: false`.
- Dropdown columns must source values from `Config!` ranges or an explicit named range formula.
- Division formulas must use an `IF` guard, for example `=IF(C2=0,0,B2/C2)`.
- Do not use volatile or external formulas such as `INDIRECT`, `OFFSET`, `NOW`, `RAND`, `WEBSERVICE`, or HTTP hyperlinks.
- Conditional formatting must use semantic colors from `assets/template-policy.json`.
- Named ranges must point to sheet cell ranges such as `Config!$A$2:$A$50`.
- `Config` must clearly tell users it is editable.

## Output Shape

For human review, return Markdown with these sections:

1. `Summary`
2. `Sheets`
3. `Columns`
4. `Named Ranges`
5. `Validation`
6. `Handoff`

For renderer handoff, return YAML-like output from the compiler and do not add prose inside the machine block.

## Edge Cases

- Missing dropdown values: create placeholder `Config` columns and mark the validation row as `warn` with the missing source named.
- Unknown renderer: set `handoff.renderer` to `xlsx-renderer` and put renderer assumptions in `handoff.notes`.
- KPI target can be zero: every attainment formula must guard the denominator with `IF(C2=0,0,...)`.
- Too many KPI categories for one dashboard: keep required sheets and add category columns instead of creating ad hoc sheet names unless the user asks.
- Requested charts or sparklines: document them as renderer handoff notes; this skill validates structure and formulas, not binary chart objects.

## Good vs Bad

Good formula:

```text
=IF(C2=0,0,B2/C2)
```

Bad formula:

```text
=B2/C2
```

Good dropdown source:

```text
Config!A2:A50
```

Bad dropdown source:

```text
Owners!A:A
```

## Validation Gate

- [ ] Required sheets exist for the chosen template type.
- [ ] Every column has `header`, `width`, `type`, and `description`.
- [ ] Dropdown columns reference `Config!` or a named range formula.
- [ ] Formula columns start with `=` and pass formula-policy checks.
- [ ] Division formulas use `IF` guards.
- [ ] Conditional formatting uses approved semantic colors.
- [ ] Data sheets avoid merged cells and declare print areas.
- [ ] Named ranges are workbook-safe and point to cell ranges.
- [ ] Validation rows include status and evidence.
- [ ] Handoff names the renderer, output format, and rendering notes.
