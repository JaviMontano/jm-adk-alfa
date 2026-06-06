# Brand DOCX - Body of Knowledge

## Canon

Brand DOCX is deterministic when every document style decision traces to a
brand token, fallback token, or explicit user instruction. A valid artifact is a
real DOCX ZIP package with required Word parts, core properties, branded styles,
footer metadata, and no remote dependency.

## Required Invariants

- Output is a DOCX package, not HTML renamed as `.docx`.
- Required ZIP parts include content types, relationships, core properties,
  document XML, and styles XML.
- Brand colors and fonts come from config or fallback assets.
- Caller supplies artifact date and footer year; current date is not inferred.
- Tables use branded header styling when tables are present.
- Remote assets, remote fonts, base64 images, unresolved placeholders, and
  random values are not allowed.

## False Positives

- HTML landing pages route to `brand-html`.
- XLSX spreadsheet requests route to `brand-xlsx`.
- Slide deck requests route to a presentation workflow.
- Token extraction without DOCX output routes away.

## Validation

Use `scripts/validate_brand_docx.py` and fixture JSON to verify package
contract behavior before marking DoD complete.
