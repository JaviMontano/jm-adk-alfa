---
name: github-actions-ci-deep
type: execution
version: 2.0.0
description: "Full GitHub Actions CI/CD design for complex pipelines."
---

# Deep CI/CD Design

Use when the pipeline includes matrices, caches, deploys, releases, protected
environments, self-hosted runners, reusable workflows, or multiple packages.

## Steps

1. Build the pipeline surface from repository evidence.
2. Define trigger policy with `assets/triggers-policy.json`.
3. Define job graph, permissions, actions, cache, matrix, secrets, and deploy
   gates with the corresponding assets.
4. Produce the output sections in `assets/ci-workflow-contract.json`.
5. For JSON output, validate with `scripts/validate_github_actions_ci.py`.

## Output

Return a complete workflow plan with safety gates, validation evidence,
assumptions, blocked settings, and Guardian decision.
