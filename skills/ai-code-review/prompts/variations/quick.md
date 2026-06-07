---
name: ai-code-review-quick
type: variation
version: 2.1.0
description: "Quick deterministic AI Code Review mode."
---

# AI Code Review - Quick Mode

Use quick mode for small diffs or targeted files.

Rules:
- inspect only the requested scope
- report only P0-P2 issues with clear file-line evidence
- include no more than five findings
- mark tests as `not-run` unless commands were executed
- include one sentence for residual risk
