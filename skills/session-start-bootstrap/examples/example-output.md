# Example Output

## Environment

- [CONFIG] Active brand: JM Labs.
- [CODE] Repo: `/Users/deonto/Documents/workspace/jm-adk-alfa`.
- [CODE] Branch: `main`.
- [CODE] `git status --short --branch` returned `## main...origin/main`.

## Context Sources Loaded

- [DOC] Root `AGENTS.md`.
- [CONFIG] User-provided workflow queue and pause criteria.
- [CODE] Prior ReleasePacket from the previous skill.

## Active Guardrails

- [CONFIG] Exactly one skill, one branch, one PR, one green merge at a time.
- [CONFIG] Stop on local changes, open PRs, failed validation, CI failure, or
  cross-skill dependency.

## Current State

- [CODE] No open PRs were listed by `gh pr list`.
- [CODE] `main`, `origin/main`, `HEAD`, and remote `main` match.

## Blockers And Gaps

- [OPEN] No blockers after preflight.

## Validation Baseline

| Command | Status | Evidence |
|---|---|---|
| `git status --short --branch` | pass | [CODE] clean branch output |

## First Action

- [CONFIG] Create `codex/harden-session-start-bootstrap-dod-20260606` from
  `origin/main`.

## Guardian Decision

- [CONFIG] Pass: environment is clean and startup guardrails are explicit.
