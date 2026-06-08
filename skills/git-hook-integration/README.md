<!--
generated-by: scripts/scaffold-skill.py
generated-for: git-hook-integration
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Git Hook Integration

Design repository-local Git hook plans that combine pre-commit checks, commit
message enforcement, and pre-push quality gates without installing hooks unless
the user explicitly asks for that mutation.

## Triggers

- git-hook-integration

## Allowed Tools

- Read
- Write
- Glob
- Grep
- Bash

## Quick Use

Use this skill when a repository needs Git hook coverage for quality gates,
Conventional Commits, or local validation workflows. Prefer the deterministic
compiler when the user can provide or accept structured JSON input.

## Deterministic Bundle

- `assets/git-hook-integration-schema.json` defines the required input shape.
- `assets/hook-stage-model.json` defines required hook stages and purposes.
- `assets/conventional-commit-policy.json` defines commit message policy.
- `assets/install-strategy-model.json` keeps installation plans explicit.
- `assets/validation-command-catalog.json` names validation command categories.
- `scripts/compile-git-hook-integration.py` renders a Markdown plan from JSON.
- `scripts/check.sh` verifies valid and invalid fixtures.

## Output Format

Markdown with summary, evidence, hook matrix, Conventional Commit policy,
validation commands, installation plan, validation, and risks.
