---
name: brand-html
version: 1.1.0
description: >
  Generate deterministic, brand-token-compliant single-file HTML artifacts from
  a supplied brand configuration or explicit fallback defaults. The skill
  enforces CSS variables, semantic structure, responsive CSS, accessibility,
  contrast, dependency boundaries, and offline validation fixtures. [EXPLICIT]
  Trigger: "generate branded HTML", "create a landing page", "build a
  brand-compliant web page", "produce a styled HTML report", "design a
  responsive page", "brand tokens", "CSS variables", "HTML generation"
argument-hint: "page-type [brand-config-path]"
model: opus
context: fork
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Bash
---

# Brand HTML / Web Generation

## Purpose

Generate self-contained, accessible, responsive HTML/CSS artifacts that are
deterministically tied to a brand configuration. The skill may write the
requested HTML artifact, but validation is read-only and must pass the local
contract before delivery. [CONFIG]

## Deterministic Resources

- `assets/manifest.json` declares all deterministic assets. [CÓDIGO]
- `assets/activation-policy.json` defines activation, routing, and false
  positives. [CÓDIGO]
- `assets/brand-html-contract.json` defines required artifact structure,
  dependency boundaries, token rules, and validator checks. [CÓDIGO]
- `assets/favicon-policy.json` and `assets/favicon.svg` define deterministic
  browser favicon behavior. [CÓDIGO]
- `assets/fallback-brand-config.json` defines explicit fallback tokens when no
  brand config is supplied. [CÓDIGO]
- `assets/evidence-policy.json` defines evidence tags and report requirements.
  [CÓDIGO]
- `scripts/check.sh` validates valid and invalid HTML fixtures offline. [CÓDIGO]

## When To Activate

Activate when the user asks for a branded HTML page, landing page, responsive
web page, styled HTML report, single-file web artifact, CSS-variable brand page,
or HTML generated from brand tokens. [CONFIG]

Do not activate for DOCX, XLSX, PDF, slides, token extraction-only tasks, or
generic brand strategy without an HTML artifact request. Route those to the
appropriate document or brand skill. [CONFIG]

## Inputs

- Page type, content outline, or report sections.
- Brand config path or inline brand tokens.
- Optional language and direction (`ltr` or `rtl`).
- Optional caller-supplied `artifact_date`; do not infer current date.
- Optional permission for external font links; default is no external
  dependencies.

## Brand Configuration

Search order:

1. Path passed as argument.
2. `./brand-config.json` in the working directory.
3. `references/brand/design-tokens.json` when the current repo brand applies.
4. `assets/fallback-brand-config.json` when no brand config exists.

Never read `~/.claude/brand-config.json` or hidden user-level files for this
skill. [CONFIG]

Required token groups:

```json
{
  "brand": { "name": "", "wordmark": "", "tagline": "" },
  "colors": { "primary": "", "black": "", "white": "", "background": "", "muted": "" },
  "typography": { "display": "", "body": "", "mono": "", "fontLinks": [] },
  "spacing": { "radiusSm": "", "radiusMd": "", "radiusLg": "", "maxWidth": "" }
}
```

## Output Contract

Return exactly one HTML artifact or one Markdown response containing exactly one
fenced `html` block. The HTML must include:

- `<!DOCTYPE html>`, `<html lang="...">`, `<head>`, `<style>`, and `<main>`.
- `<link rel="icon" type="image/svg+xml" href="...">` in `<head>`.
- CSS variables for every brand color and font used.
- Semantic landmarks: `<header>`, `<nav>` when navigation exists, `<main>`,
  `<section>`, and `<footer>`.
- Responsive CSS with at least one `@media` query.
- No unresolved `{{PLACEHOLDER}}` tokens.
- No base64 images.
- No external JavaScript.
- No remote font links unless the supplied config explicitly allows them.
- No current date/time unless `artifact_date` is supplied.
- Favicon must be SVG, square/self-contained, not remote, and not base64.

## Token Rules

- Use CSS variables such as `--brand-primary`, `--brand-bg`, `--brand-black`,
  `--brand-white`, `--brand-muted`, `--font-display`, and `--font-body`.
- Hardcoded hex colors are allowed only inside the `:root` token declaration or
  in the explicit fallback config comment. [CONFIG]
- Reuse token variables everywhere else.
- Fallback defaults are `#2563EB`, `#0F172A`, `#FFFFFF`, `#F8FAFC`, `#475569`,
  and `system-ui`.

## Accessibility And Layout

- Body text contrast must be at least WCAG AA when deterministically checkable.
- Use semantic headings in order.
- Avoid ALL CAPS headings.
- Include responsive constraints for grids/cards.
- For RTL content, set `dir="rtl"` on `<html>` and use logical CSS properties
  where possible.

## Validation Gate

- [ ] Brand config or fallback tokens are explicitly declared.
- [ ] CSS variables are present and used.
- [ ] HTML is single-file and self-contained.
- [ ] SVG favicon link exists and is deterministic.
- [ ] No remote assets unless explicitly allowed by config.
- [ ] No base64 images or external JavaScript.
- [ ] No unresolved placeholders.
- [ ] Semantic landmarks exist.
- [ ] Responsive CSS exists.
- [ ] Contrast gate passes or records a deterministic limitation.
- [ ] `bash skills/brand-html/scripts/check.sh` passes.

## Assumptions & Limits

- This skill creates HTML/CSS only; it does not build SPAs, routing, databases,
  DOCX, XLSX, PDF, or slide decks. [CONFIG]
- External fonts are disabled by default because deterministic delivery prefers
  self-contained artifacts. [CONFIG]
- Visual QA beyond static validation still requires browser inspection when the
  user asks for rendered fidelity. [CONFIG]

## Usage

- `/brand-html landing-page ./brand-config.json`
- `Generate a responsive branded HTML report using these tokens`
- `Create RTL branded HTML for Arabic content`
