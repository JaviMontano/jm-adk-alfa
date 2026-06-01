<!--
generated-by: scripts/scaffold-skill.py
generated-for: font-optimization
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

La pagina tiene riesgo de FOIT/FOUT por carga runtime de Google Fonts, `@import` render-blocking y una fuente `.ttf` no optimizada.

## Findings

| Finding | Evidence | Action |
|---|---|---|
| Runtime Google Fonts | `fonts.googleapis.com` en `<link>` | Self-host WOFF2 |
| CSS import | `@import url(...)` | Reemplazar por `@font-face` local |
| Legacy TTF | `/fonts/legacy.ttf` | Convertir/subset a WOFF2 |

## Assets Used

- `assets/font-face-template.css`
- `assets/preload-snippet.html`
- `assets/font-budget.json`

## Validation

- `scripts/audit-font-loading.py` falla sobre fixture no optimizado.
- `scripts/audit-font-loading.py` pasa sobre fixture WOFF2 con preload y `font-display: swap`.
- Output final no usa runtime font CDN.
