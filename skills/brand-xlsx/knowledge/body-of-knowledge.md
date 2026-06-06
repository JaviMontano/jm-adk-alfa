# Brand XLSX - Body of Knowledge

## Canon

Brand XLSX is deterministic when every workbook style decision traces to a
brand token, fallback token, or explicit user instruction. A valid artifact is a
real XLSX ZIP package with required workbook parts, core properties, branded
styles, meaningful sheet names, workbook features, footer metadata, and no
remote dependency.

## Required Invariants

- Output is an XLSX package, not HTML/CSV renamed as `.xlsx`.
- Required ZIP parts include content types, relationships, core properties,
  workbook XML, workbook relationships, styles XML, and worksheet XML.
- Brand colors and fonts come from config or fallback assets.
- Caller supplies artifact date, footer year, and domain; current date is not
  inferred.
- Sheet names are meaningful and not `Sheet1`.
- Tab color, title bar, headers, alternating rows, and footer use brand tokens.
- Freeze panes, auto filter, merged title/footer, and bounded column widths are
  present.
- Remote assets, remote fonts, base64 images, unresolved placeholders, and
  random values are not allowed.

## False Positives

- HTML landing pages route to `brand-html`.
- DOCX document requests route to `brand-docx`.
- Slide deck requests route to a presentation workflow.
- CSV-only exports route away.
- Token extraction without XLSX output routes away.

## Validation

Use `scripts/validate_brand_xlsx.py` and fixture JSON to verify workbook
contract behavior before marking DoD complete.
