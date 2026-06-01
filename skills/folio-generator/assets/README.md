# Folio Generator Assets

These assets are used to render branded folio documents without rebuilding styling or design tokens from memory.

## Files

- `folio-style.css`: print-safe CSS for business folio HTML.
- `brand-tokens.json`: neutral default design tokens for the folio template.
- `manifest.json`: machine-readable asset inventory and usage map.

## Contract

- Keep assets deterministic and portable.
- Do not include customer data, secrets, or real signatures.
- Update `manifest.json` whenever an asset is added, removed, or repurposed.
