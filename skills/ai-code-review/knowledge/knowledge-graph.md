# AI Code Review - Knowledge Graph

## Core Concepts
- [[ai-code-review]] - deterministic review workflow
- [[review-scope]] - included files, excluded files, and reviewed basis
- [[file-line-evidence]] - exact file and line citation for each finding
- [[severity-policy]] - P0-P3 priority contract
- [[false-positive-filter]] - confidence and suppression policy
- [[no-fake-test-results]] - command evidence required for test claims
- [[review-report-contract]] - JSON packet validated offline

## Flow
`review-scope` -> `file-line-evidence` -> `false-positive-filter` -> `severity-policy` -> `review-report-contract` -> `offline-validator`

## Tags
#ai-code-review #jm-labs #deterministic-review #code-quality
