# Font Optimization Assets

These assets provide deterministic snippets and thresholds for web font optimization work.

## Files

- `font-face-template.css`: self-hosted `@font-face` pattern with `font-display: swap`.
- `preload-snippet.html`: critical WOFF2 preload pattern.
- `font-budget.json`: default payload and loading policy thresholds.
- `manifest.json`: machine-readable asset inventory and usage map.

## Contract

- Assets must avoid network font imports.
- Assets must prefer WOFF2 and self-hosted paths.
- Update `manifest.json` whenever a snippet, budget, or usage target changes.
