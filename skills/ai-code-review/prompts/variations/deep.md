---
name: ai-code-review-deep
type: variation
version: 2.1.0
description: "Deep deterministic AI Code Review mode."
---

# AI Code Review - Deep Mode

Use deep mode when merge risk is high, security matters, or the diff crosses
multiple modules.

Additional checks:
- compare changed behavior against tests and documentation
- inspect call sites for contract changes
- review authorization, input validation, secrets, and persistence paths
- identify missing regression tests tied to changed behavior
- record non-findings when a tempting issue is intentionally suppressed

Output must still separate confirmed findings from `needs-verification` items.
