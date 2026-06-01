# Font Optimization — Body of Knowledge

## Canon

Font optimization reduces render-blocking font work while preserving brand typography. The default target is visible text on first paint, no runtime font CDN dependency in optimized output, WOFF2-only delivery, and critical font payload under the budget in `assets/font-budget.json`.

## Loading Rules

| Rule | Target |
|---|---|
| Critical format | WOFF2 |
| Critical preload | `<link rel="preload" as="font" type="font/woff2" crossorigin>` |
| Body copy display | `font-display: swap` |
| Decorative/non-critical display | `font-display: optional` |
| Runtime CDN | Avoid Google Fonts or other runtime font CSS imports in final output |
| CSS import | Avoid `@import` for fonts |

## Audit Rules

- Run `scripts/audit-font-loading.py` on HTML/CSS outputs.
- Treat `google_fonts_runtime`, `css_import`, `font_display_block`, `non_woff2_font`, `missing_font_display`, `missing_woff2`, and `missing_preload` as fix-required findings.
- Use `assets/font-face-template.css` for self-hosted declarations.
- Use `assets/preload-snippet.html` for critical font preload.

## Quality Metrics

| Metric | Target | How to Measure |
|--------|--------|---------------|
| Critical font payload | <= 100KB | Sum WOFF2 files required for above-the-fold text |
| Runtime CDN imports | 0 | Static audit of HTML/CSS |
| FOIT risk | 0 block display declarations | Static audit + visual smoke |
| Critical preload coverage | 100% for critical fonts | Static audit |
| Evidence coverage | 100% | Claims cite code/config/test output |
