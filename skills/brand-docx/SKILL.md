---
name: brand-docx
version: 1.1.0
description: >
  Generate deterministic, brand-token-compliant Microsoft Word DOCX artifacts
  from supplied brand configuration or explicit fallback defaults. Use when the
  user asks for a Word document, DOCX, branded proposal, branded report, cover
  page, or python-docx output. The skill enforces real DOCX package structure,
  core properties, brand tokens, table/header/footer styling, no remote assets,
  no unresolved placeholders, and offline validator fixtures. [EXPLICIT]
argument-hint: "document-type title [brand-config-path]"
model: opus
context: fork
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Bash
---

# Brand DOCX / Word Document Generation

## Purpose

Generate `.docx` artifacts that are deterministic, brand-token-compliant, and
validated as real Word packages. The skill may write the requested DOCX
artifact, but validation must stay offline and must pass the local contract
before delivery. [CONFIG]

## Deterministic Resources

- `assets/manifest.json` declares all deterministic assets. [CÓDIGO]
- `assets/activation-policy.json` defines activation, routing, and false
  positives. [CÓDIGO]
- `assets/brand-docx-contract.json` defines required DOCX package parts,
  metadata, dependency boundaries, token rules, and validator checks. [CÓDIGO]
- `assets/fallback-brand-config.json` defines explicit fallback tokens when no
  brand config is supplied. [CÓDIGO]
- `assets/style-token-map.json` maps brand tokens to Word styles. [CÓDIGO]
- `assets/evidence-policy.json` defines evidence tags and report requirements.
  [CÓDIGO]
- `scripts/check.sh` validates valid and invalid DOCX fixtures offline.
  [CÓDIGO]

## When To Activate

Activate when the user asks for a Word document, `.docx`, branded proposal,
branded report, branded memo, cover page, python-docx generation, or a file
intended to open in Microsoft Word. [CONFIG]

Do not activate for HTML pages, XLSX spreadsheets, PDFs, slide decks, image
assets, or token extraction-only tasks. Route those requests to the appropriate
document or brand skill. [CONFIG]

## Inputs

- Document type: proposal, report, memo, case study, brief, or cover page.
- Title, subtitle, section outline, tables, and footer requirements.
- Brand config path or inline brand tokens.
- Optional language and page size.
- Optional caller-supplied `artifact_date` and `year`; do not infer current
  date/time.
- Optional confidentiality flag.

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
  "colors": { "primary": "", "black": "", "white": "", "background": "", "muted": "" },
  "typography": { "display": "", "body": "", "fallback": "" },
  "docx": { "artifact_date": "", "year": "", "confidential": false }
}
```

## Output Contract

Return exactly one of these outputs:

- A saved `.docx` artifact path plus validation evidence.
- A plan for generating the `.docx` when the user asks for instructions only.

The delivered `.docx` must include:

- Real DOCX ZIP package structure, not HTML renamed as `.docx`.
- `[Content_Types].xml`, `_rels/.rels`, `docProps/core.xml`,
  `word/document.xml`, and `word/styles.xml`.
- Core properties with title, creator, and caller-supplied artifact date.
- Cover or opening section with wordmark, title, tagline, and document type.
- Section headings styled from brand display font and primary underline.
- Body text styled from brand body font and black/muted tokens.
- Tables with primary header fill and white header text when tables exist.
- Footer metadata with caller-supplied year and confidentiality label when
  requested.
- No unresolved `{{PLACEHOLDER}}` tokens.
- No remote fonts, remote logos, remote images, base64 images, external scripts,
  runtime current-date calls, or random values.

## Token Rules

- Use supplied brand tokens or explicit fallback tokens only.
- Do not hardcode legacy palettes such as `#122562`, `#FFD700`, or `#137DC5`
  unless they are explicitly supplied in the active brand config. [CONFIG]
- Fallback defaults are `#2563EB`, `#0F172A`, `#FFFFFF`, `#F8FAFC`,
  `#475569`, `Aptos Display`, and `Aptos`.
- Preserve tokens in generated styles so validation can trace them.

## Validation Gate

- [ ] Brand config or fallback tokens are explicitly declared.
- [ ] Output is a real `.docx` package, not HTML or Markdown.
- [ ] Required DOCX ZIP parts exist.
- [ ] Core properties include caller-supplied title/date.
- [ ] Brand colors and fonts are present in document XML/styles.
- [ ] Tables, if present, use deterministic branded header styling.
- [ ] Footer metadata includes caller-supplied year and confidentiality state.
- [ ] No unresolved placeholders.
- [ ] No remote assets, base64 images, runtime dates, or randomness.
- [ ] `bash skills/brand-docx/scripts/check.sh` passes.

## Assumptions And Limits

- This skill creates DOCX/Word artifacts only; it does not build HTML pages,
  XLSX spreadsheets, PDFs, or slide decks. [CONFIG]
- `python-docx` is a suitable implementation path when available, but the
  validation gate uses the Python standard library so CI remains deterministic.
  [CONFIG]
- Word rendering can vary by installed fonts; fallback fonts must be specified.
  [INFERENCIA]

## Usage

- `/brand-docx proposal "AtlasOps Technical Proposal" ./brand-config.json`
- `Generate a branded DOCX report with a cover page and KPI table`
- `Use python-docx to create a Word proposal using these brand tokens`
