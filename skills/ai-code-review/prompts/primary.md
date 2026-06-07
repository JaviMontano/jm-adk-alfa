---
name: ai-code-review-primary
type: execution
version: 2.1.0
description: "Execute deterministic AI Code Review with source-backed findings."
triad:
  lead: "ai-code-review-lead"
  support: "ai-code-review-support"
  guardian: "ai-code-review-guardian"
---

# AI Code Review - Execute

## Dynamic Parameters
| Parameter | Description | Required | Filled By |
|-----------|-------------|----------|-----------|
| `{{task}}` | Review request | Yes | User input |
| `{{scope}}` | Files, diff, branch, or directory under review | Yes | User or repository |
| `{{constraints}}` | Focus areas and exclusions | No | User or assets |
| `{{depth}}` | quick / standard / deep / adversarial | No | Auto |
| `{{output_format}}` | markdown / json / both | No | Auto |

## Execution
1. Load `knowledge/body-of-knowledge.md`.
2. Load assets: severity, evidence, scope, false-positive, and report contract.
3. Lead establishes scope and reads changed files.
4. Lead drafts findings only with exact evidence.
5. Support removes false positives and groups duplicate root causes.
6. Guardian validates file-line evidence, priority, confidence, and test-result claims.
7. For JSON output, validate with `scripts/validate_ai_code_review_report.py` when a packet is available.

## Output
- Review summary and scope.
- Findings sorted by P0, P1, P2, P3.
- Each finding: file, line, category, evidence, impact, recommendation, confidence.
- Validation commands actually run, or `claimed_test_status: not-run`.
- Remaining risks and review limits.
