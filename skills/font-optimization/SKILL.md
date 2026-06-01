---
name: font-optimization
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Optimize web font loading with subsetting, preloading, font-display strategies,
  and variable fonts to eliminate FOIT/FOUT and improve performance. [EXPLICIT]
  Trigger: "font loading", "web fonts", "FOIT", "font-display", "variable fonts"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Font Optimization

> "Typography is the voice of design — make sure it doesn't stutter on load." — Unknown

## TL;DR

Guides web font optimization to eliminate invisible text (FOIT) and layout shifts (FOUT) — covers font-display strategies, preloading critical fonts, Unicode range subsetting, variable fonts for weight reduction, and self-hosting vs CDN tradeoffs. Use when custom fonts are causing performance issues or layout shifts. [EXPLICIT]

## Procedure

### Step 1: Discover
- Inventory all fonts in use (families, weights, styles)
- Measure font impact on CLS and FCP with Lighthouse
- Check current loading method (Google Fonts CDN, self-hosted, @import)
- Identify which fonts are critical (above-the-fold) vs decorative

### Step 2: Analyze
- Determine minimum character set needed (latin, latin-ext, specific glyphs)
- Evaluate variable font availability (one file replaces multiple weight files)
- Plan font-display strategy (`swap` for body, `optional` for non-critical)
- Calculate total font payload and compare with subsetting savings
- Use `assets/font-budget.json` for default payload and critical-file thresholds

### Step 3: Execute
- Self-host fonts for better performance (eliminate third-party DNS lookup)
- Subset fonts to only needed Unicode ranges using `glyphhanger` or `pyftsubset`
- Implement `font-display: swap` in `@font-face` declarations
- Preload critical fonts: `<link rel="preload" href="font.woff2" as="font" crossorigin>`
- Use WOFF2 format exclusively (best compression, 95%+ browser support)
- Replace multiple weight files with a single variable font where possible
- Use `assets/font-face-template.css` and `assets/preload-snippet.html` for reusable implementation snippets

### Step 4: Validate
- Confirm no FOIT — text is always visible during font loading
- Measure CLS impact — font swap should cause minimal layout shift
- Verify font files are cached with long-lived Cache-Control headers
- Check total font payload is under 100KB for all critical fonts
- Run `scripts/audit-font-loading.py <html-or-css-files>` on changed templates or pages

## Quality Criteria

- [ ] All fonts served in WOFF2 format
- [ ] Critical fonts preloaded with `rel="preload"`
- [ ] `font-display` set appropriately for each font family
- [ ] Font files subsetted to required character ranges only
- [ ] No runtime Google Fonts/CDN import remains in optimized output
- [ ] `assets/manifest.json` declares every reusable output asset
- [ ] `scripts/audit-font-loading.py` returns zero findings on optimized fixtures
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Loading 6+ font weights when the design only uses 2-3
- Using `@import` in CSS to load Google Fonts (render-blocking)
- Setting `font-display: block` which causes invisible text during load

## Related Skills

- `performance-testing` — measuring font loading impact on Core Web Vitals
- `build-optimization` — automating font subsetting in the build pipeline

## Usage

Example invocations:

- "/font-optimization" — Run the full font optimization workflow
- "font optimization on this project" — Apply to current context

## Deterministic Script Contract

- Runtime script: `scripts/audit-font-loading.py`
- Contract check: `scripts/check.sh`
- Validation command: `python3 scripts/validate-skill-scripts.py --strict --run-checks --skill font-optimization`
- Default behavior: read-only audit, no network calls, nonzero exit on findings.

## Assets Contract

- Output assets live in `assets/`.
- `assets/manifest.json` lists every reusable asset and where it is used.
- `assets/font-face-template.css` is the canonical self-hosted WOFF2 `@font-face` pattern.
- `assets/preload-snippet.html` is the canonical critical preload snippet.
- `assets/font-budget.json` carries default performance budgets and required patterns.


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
