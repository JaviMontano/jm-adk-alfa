<!--
generated-by: scripts/scaffold-skill.py
generated-for: git-hook-integration
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

- [CODE] Hook manager: native-git.
- [CODE] Install mode: plan-only.
- [CODE] Hook directory: .githooks.
- [CODE] Conventional commits: enabled.

## Hook Matrix

| Stage | Hook | Blocking | Command | Purpose |
|---|---|---|---|---|
| pre-commit | quality-fast | True | `bash scripts/pre-tool-guard.sh && git diff --check` | Block dangerous local changes and whitespace errors before commit. |
| commit-msg | conventional-commit | True | `python3 scripts/validate-commit-message.py "$1"` | Enforce Conventional Commit headers. |
| pre-push | quality-full | True | `python3 scripts/count-components.py --check-docs && python3 scripts/validate-skills.py --strict` | Block publication when component counts or skill validation fail. |

## Installation Plan

- [CODE] Strategy: native-git.
- [CODE] Install command: `git config core.hooksPath .githooks`.
- [CODE] Requested mode: plan-only.

## Validation

- [CODE] Required hook stages present: commit-msg, pre-commit, pre-push.
- [CODE] Conventional Commit policy is backed by a commit-msg hook.
- [CODE] Validation commands map to declared hook stages.
- [CODE] Hook commands are rendered as plan output; the compiler does not install hooks.

## Risks And Limits

- [INFERENCE] Hook plans still require repository-specific review before installation.
- [INFERENCE] Developers can bypass Git hooks with --no-verify unless server-side protection exists.
- [ASSUMPTION] Commands supplied in input are trusted project-local validation commands.
