# Font Optimization Scripts

Deterministic local audit for web font loading patterns.

## Entry Points

- `audit-font-loading.py`: scans HTML/CSS files for runtime font CDNs, `@import`, missing preload, missing `font-display`, and non-WOFF2 font references.
- `check.sh`: validates fixtures, expected failures, expected passes, and JSON output.

## Contract

- The audit is read-only.
- The audit never fetches remote font files.
- A nonzero exit means the inspected files still contain font-loading issues.
- Budgets and required patterns live in `assets/font-budget.json`.
