# Brand XLSX Package Template

## Required Package Parts

- `[Content_Types].xml`
- `_rels/.rels`
- `docProps/core.xml`
- `xl/workbook.xml`
- `xl/_rels/workbook.xml.rels`
- `xl/styles.xml`
- `xl/worksheets/sheet1.xml`

## Required Content

- Core title: `[TITLE]`
- Creator: `brand-xlsx`
- Artifact date: `[CALLER_SUPPLIED_ARTIFACT_DATE]`
- Sheet name: `[MEANINGFUL_SHEET_NAME]`
- Tab color: `[BRAND_PRIMARY]`
- Footer: `[WORDMARK] | [TAGLINE] | [YEAR] | [DOMAIN]`

## Style Tokens

- Title bar: `colors.primary` fill and `colors.black` text
- Subtitle bar: `colors.black` fill and `colors.primary` text
- Column header: `colors.black` fill and `colors.primary` text
- Even rows: `colors.white` fill and `colors.black` text
- Odd rows: `colors.background` fill and `colors.black` text
- Footer: `colors.black` fill and `colors.muted` text

## Guardrails

- Use caller-supplied dates only.
- Use config or fallback tokens only.
- Reject remote assets and renamed HTML/CSV.
