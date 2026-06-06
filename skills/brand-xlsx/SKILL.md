---
name: brand-xlsx
version: 1.1.0
description: >
  Generate deterministic, brand-token-compliant Microsoft Excel XLSX artifacts
  from supplied brand configuration or explicit fallback defaults. Use when the
  user asks for an Excel workbook, XLSX, branded spreadsheet, spreadsheet
  report, KPI dashboard, or openpyxl output. The skill enforces real XLSX
  package structure, workbook/core properties, sheet names, tab colors, merged
  title/footer regions, brand-token styles, freeze panes, bounded column
  widths, no remote assets, no unresolved placeholders, and offline validator
  fixtures. [EXPLICIT]
argument-hint: "sheet-title [brand-config-path]"
model: opus
context: fork
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Bash
---

# Brand XLSX / Excel Workbook Generation

## Purpose

Generate `.xlsx` artifacts that are deterministic, brand-token-compliant, and
validated as real Excel packages. The skill may write the requested XLSX
artifact, but validation must stay offline and must pass the local contract
before delivery. [CONFIG]

## Deterministic Resources

- `assets/manifest.json` declares all deterministic assets. [CÓDIGO]
- `assets/activation-policy.json` defines activation, routing, and false
  positives. [CÓDIGO]
- `assets/brand-xlsx-contract.json` defines required XLSX package parts,
  workbook features, dependency boundaries, token rules, and validator checks.
  [CÓDIGO]
- `assets/fallback-brand-config.json` defines explicit fallback tokens when no
  brand config is supplied. [CÓDIGO]
- `assets/style-token-map.json` maps brand tokens to workbook styles. [CÓDIGO]
- `assets/evidence-policy.json` defines evidence tags and report requirements.
  [CÓDIGO]
- `scripts/check.sh` validates valid and invalid XLSX fixtures offline.
  [CÓDIGO]

## When To Activate

Activate when the user asks for an Excel workbook, `.xlsx`, branded
spreadsheet, spreadsheet report, KPI dashboard, openpyxl generation, or a file
intended to open in Microsoft Excel. [CONFIG]

Do not activate for CSV-only exports, HTML pages, DOCX documents, PDFs, slide
decks, image assets, or token extraction-only tasks. Route those requests to
the appropriate document or brand skill. [CONFIG]

## Inputs

- Workbook type: report, KPI dashboard, inventory table, financial summary, or
  operational workbook.
- Title, subtitle, sheet name, headers, rows, KPI blocks, and footer needs.
- Brand config path or inline brand tokens.
- Optional caller-supplied `artifact_date`, `year`, and `domain`; do not infer
  current date/time.
- Optional wide-data and print/freeze-pane requirements.

## Brand Configuration

Search order:

1. Path passed as argument.
2. `./brand-config.json` in the working directory.
3. `references/brand/design-tokens.json` when the current repo brand applies.
4. `assets/fallback-brand-config.json` when no brand config exists.

Never read hidden user-level brand files for this skill. [CONFIG]

Required token groups:

```json
{
  "brand": { "name": "", "wordmark": "", "tagline": "" },
  "colors": { "primary": "", "black": "", "white": "", "background": "", "muted": "", "primarySoft": "" },
  "typography": { "body": "" },
  "xlsx": { "artifact_date": "", "year": "", "domain": "" }
}
```

## Output Contract

Return exactly one of these outputs:

- A saved `.xlsx` artifact path plus validation evidence.
- A plan for generating the `.xlsx` when the user asks for instructions only.

The delivered `.xlsx` must include:

- Real XLSX ZIP package structure, not HTML or CSV renamed as `.xlsx`.
- `[Content_Types].xml`, `_rels/.rels`, `docProps/core.xml`,
  `xl/workbook.xml`, `xl/_rels/workbook.xml.rels`, `xl/styles.xml`, and at
  least one `xl/worksheets/sheet*.xml`.
- Core properties with title, creator, and caller-supplied artifact date.
- Meaningful sheet names, not `Sheet1`.
- Primary tab color.
- Merged title region, header row, data rows, and footer metadata.
- Brand colors and fonts in `xl/styles.xml`.
- Freeze panes, auto filter, and bounded column widths.
- Footer metadata with wordmark, tagline, caller-supplied year, and domain.
- No unresolved `{{PLACEHOLDER}}` tokens.
- No remote fonts, remote logos, remote images, base64 images, external
  relationships, runtime current-date calls, or random values.

## Token Rules

- Use supplied brand tokens or explicit fallback tokens only.
- Do not hardcode legacy palettes such as `#122562`, `#FFD700`, `#137DC5`, or
  `#FF7E08` unless they are explicitly supplied in the active brand config.
  [CONFIG]
- Fallback defaults are `#2563EB`, `#0F172A`, `#FFFFFF`, `#F8FAFC`,
  `#475569`, `#EFF6FF`, and `Calibri`.
- Preserve tokens in generated styles so validation can trace them.

## Validation Gate

- [ ] Brand config or fallback tokens are explicitly declared.
- [ ] Output is a real `.xlsx` package, not HTML/CSV/Markdown.
- [ ] Required XLSX ZIP parts exist.
- [ ] Core properties include caller-supplied title/date.
- [ ] Sheet names are meaningful.
- [ ] Tab color uses primary token.
- [ ] Title/footer regions are merged.
- [ ] Headers, alternating rows, and footer use deterministic branded styles.
- [ ] Freeze panes, auto filter, and bounded column widths are present.
- [ ] No unresolved placeholders.
- [ ] No remote assets, base64 images, runtime dates, or randomness.
- [ ] `bash skills/brand-xlsx/scripts/check.sh` passes.

## Assumptions And Limits

- This skill creates XLSX/Excel artifacts only; it does not build HTML pages,
  DOCX documents, PDFs, slide decks, or CSV-only exports. [CONFIG]
- `openpyxl` is a suitable implementation path when available, but the
  validation gate uses the Python standard library so CI remains deterministic.
  [CONFIG]
- Excel rendering can vary by installed fonts; fallback font must be declared.
  [INFERENCIA]

## Usage

- `/brand-xlsx "AtlasOps KPI Workbook" ./brand-config.json`
- `Generate a branded XLSX report with KPI boxes and a data table`
- `Use openpyxl to create an Excel workbook using these brand tokens`
