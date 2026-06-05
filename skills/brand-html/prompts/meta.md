---
name: brand-html-meta
type: self-improvement
version: 2.1.0
description: "Evaluate and improve deterministic Brand HTML."
---

# Brand HTML - Self-Improvement

## Evaluate

1. Do evals cover tokenized output, fallback config, RTL, dark mode, invalid
   off-token colors, SVG favicons, low contrast, base64/external scripts, and
   false positives?
2. Do templates avoid remote dependencies and implicit current dates?
3. Does the validator reject unresolved placeholders, missing landmarks, and
   non-SVG favicon links?
4. Are fallback tokens still explicit and documented?
5. Does the ledger review doc include command evidence before `dod-complete`?

## Improve

1. Update assets before prompts/templates.
2. Add or adjust fixtures before validator changes.
3. Re-run `bash skills/brand-html/scripts/check.sh`.
4. Re-run per-skill DoD before ledger changes.
