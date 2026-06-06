---
name: brand-docx-meta
type: self-improvement
version: 2.1.0
description: "Evaluate and improve deterministic Brand DOCX."
---

# Brand DOCX - Self-Improvement

## Evaluate

1. Do evals cover real DOCX packages, fallback config, token override, metadata,
   long tables, invalid remote assets, HTML renamed as DOCX, placeholders, and
   false positives?
2. Do templates avoid remote dependencies, hidden user files, implicit current
   dates, and hardcoded legacy colors?
3. Does the validator reject non-DOCX output, unresolved placeholders, remote
   URLs, and legacy hardcoded colors?
4. Does the ledger review doc include command evidence before `dod-complete`?

## Improve

1. Update assets before prompts/templates.
2. Add or adjust fixtures before validator changes.
3. Re-run `bash skills/brand-docx/scripts/check.sh`.
4. Re-run per-skill DoD before ledger changes.
