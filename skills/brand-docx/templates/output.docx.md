# Brand DOCX Package Template

## Required Package Parts

- `[Content_Types].xml`
- `_rels/.rels`
- `docProps/core.xml`
- `word/document.xml`
- `word/styles.xml`

## Required Content

- Core title: `[TITLE]`
- Creator: `brand-docx`
- Artifact date: `[CALLER_SUPPLIED_ARTIFACT_DATE]`
- Wordmark: `[BRAND_WORDMARK]`
- Tagline: `[BRAND_TAGLINE]`
- Footer year: `[CALLER_SUPPLIED_YEAR]`
- Confidential label: `[CONFIDENTIAL_LABEL_IF_REQUESTED]`

## Style Tokens

- Cover title: `typography.display`, `colors.black`
- Section heading: `typography.display`, `colors.black`, underline
  `colors.primary`
- Body text: `typography.body`, `colors.black`
- Table header: `colors.primary` fill and `colors.white` text
- Footer metadata: `colors.muted`

## Guardrails

- Use caller-supplied dates only.
- Use config or fallback tokens only.
- Reject remote assets and renamed HTML.
