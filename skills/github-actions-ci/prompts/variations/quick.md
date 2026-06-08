---
name: github-actions-ci-quick
type: execution
version: 2.0.0
description: "Fast GitHub Actions CI review with deterministic safety gates."
---

# Quick CI Review

Use when the user needs an immediate pass, warn, or block decision on a workflow
plan.

## Steps

1. Identify triggers, jobs, permissions, actions, secrets, cache, deploy gates,
   and validation evidence.
2. Block ready status for unpinned required actions, broad permissions, inline
   secrets, missing lockfile cache keys, or PR production deploys.
3. Return the smallest change set needed to pass Guardian review.

## Output

- Decision
- Blocking checks
- Required edits
- Validation checks
