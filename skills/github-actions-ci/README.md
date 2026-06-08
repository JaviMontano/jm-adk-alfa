# GitHub Actions CI/CD

Deterministic CI/CD workflow planning for GitHub Actions.

## Triggers

- `github-actions-ci`
- `GitHub Actions`
- `CI/CD`
- `CI pipeline`
- `deploy workflow`
- `workflow permissions`
- `matrix build`

## Allowed Tools

- Read
- Write
- Glob
- Grep
- Bash

## Quick Use

Use this skill when a repository needs a GitHub Actions plan or review that can
be validated offline before writing or changing workflow YAML.

## Output Format

Markdown or JSON with:

- pipeline surface
- triggers
- jobs and dependency graph
- permissions
- action pinning
- cache policy
- matrix strategy
- secrets and environments
- deployment gates
- validation evidence
- Guardian decision

Structured JSON workflow plans can be validated offline with
`scripts/validate_github_actions_ci.py`.
