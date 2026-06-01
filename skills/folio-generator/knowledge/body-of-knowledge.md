<!--
generated-by: scripts/scaffold-skill.py
generated-for: folio-generator
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Folio Generator Body of Knowledge

## Canon

Folios are controlled business document identifiers. The canonical format is `PREFIX-YYYY-NNN`, where `PREFIX` is exactly three uppercase letters, `YYYY` is the emission year, and `NNN` is a zero-padded sequential counter.

## Prefix Registry

| Prefix | Document type | Use |
|---|---|---|
| COT | Cotizacion | Commercial proposals and budgets |
| MEM | Memorandum | Internal or external memos |
| FAC | Factura | Invoice-like controlled documents |
| MIN | Minuta | Meeting minutes or acts |
| DOC | Documento | Generic controlled document |

## State Rules

- Calculate first with `--dry-run`.
- Reserve a number only with `--apply`.
- Treat `.folio-tracker.json` as JSON state, never as plain text.
- Reject lowercase, long, short, or mixed-format prefixes.
- Validate manual folio requests against the tracker before producing a final document.

## Asset Rules

- Use `assets/folio-style.css` as the visual source for HTML folios.
- Keep design tokens in `assets/brand-tokens.json`.
- Keep `assets/manifest.json` in sync with every output asset.

## Quality Signals

| Signal | Target |
|---|---|
| Uniqueness | Next folio increments exactly once under `--apply` |
| Non-mutating preview | `--dry-run` leaves tracker byte-identical |
| Render determinism | Same JSON input and assets produce same HTML |
| Output completeness | Folio, date, recipient, subject, body, total block, signature, and footer are present |
