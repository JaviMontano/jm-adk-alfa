---
name: brand-xlsx-meta
type: self-improvement
version: 2.1.0
description: "Evaluate and improve deterministic Brand XLSX."
---

# Brand XLSX - Self-Improvement

## Evaluate

1. Do evals cover real XLSX packages, fallback config, token override,
   metadata, wide data, invalid remote assets, renamed HTML/CSV, placeholders,
   and false positives?
2. Do templates avoid remote dependencies, hidden user files, implicit current
   dates, and hardcoded legacy colors?
3. Does the validator reject non-XLSX output, missing workbook parts,
   unresolved placeholders, remote URLs, `Sheet1`, and legacy hardcoded colors?
4. Does the ledger review doc include command evidence before `dod-complete`?

## Improve

1. Update assets before prompts/templates.
2. Add or adjust fixtures before validator changes.
3. Re-run `bash skills/brand-xlsx/scripts/check.sh`.
4. Re-run per-skill DoD before ledger changes.
