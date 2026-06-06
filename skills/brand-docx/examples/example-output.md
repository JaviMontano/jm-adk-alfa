# Brand DOCX Example Output

## Summary

- Generated `AtlasOps Technical Proposal.docx` as a real DOCX package.
  [CÓDIGO]
- Applied supplied brand colors, fonts, title, year, and confidentiality flag.
  [CÓDIGO]
- Rejected remote assets, unresolved placeholders, and renamed HTML output.
  [CONFIG]

## Artifact

- Path: `AtlasOps Technical Proposal.docx` [CÓDIGO]
- Format: Microsoft Word DOCX ZIP package [CÓDIGO]
- Core title: `AtlasOps Technical Proposal` [CÓDIGO]
- Creator: `brand-docx` [CÓDIGO]
- Artifact date: `2026-06-05` [CÓDIGO]

## Validation

- Required ZIP parts exist: `[Content_Types].xml`, `_rels/.rels`,
  `docProps/core.xml`, `word/document.xml`, `word/styles.xml`. [CÓDIGO]
- Brand tokens present: `#2563EB`, `#0F172A`, `#FFFFFF`, `#F8FAFC`,
  `#475569`, `Aptos Display`, `Aptos`. [CÓDIGO]
- Footer metadata includes `CONFIDENTIAL | 2026`. [CÓDIGO]
- `bash skills/brand-docx/scripts/check.sh` passes. [CÓDIGO]

## Risks And Limits

- Installed font availability can affect visual rendering in Word; fallback
  fonts remain declared. [INFERENCIA]
