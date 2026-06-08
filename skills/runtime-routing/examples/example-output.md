# Example Output

## Summary

Recommended runtime: Codex local workspace. It has verified local file access, shell execution, git state visibility, and GitHub CLI access in the current session. Claude, Gemini, Antigravity, and VS Code adapters remain validation-pending unless their repo adapter evidence or active runtime session is inspected.

## Capability Matrix

| runtime | status | evidence | limits |
|---|---|---|---|
| Codex | verified | current workspace + `git status` + `gh pr list` | use existing local permissions only |
| VS Code | pending | adapter docs may exist | active IDE state not observed |
| Claude | pending | adapter docs may exist | active tool/session state not observed |
| Gemini | pending | adapter docs may exist | active runtime not observed |
| Antigravity | pending | adapter docs may exist | runtime validation pending |
| local-adapter | verified | repo-local scripts | may not cover UI/runtime-specific tasks |

## Decision

Use Codex for this task because it is the lowest-permission verified path that can read files, edit the repo, run validators, inspect git state, and use `gh` for PR checks.

## Fallback

If GitHub CLI auth fails, pause and mark `Dato requerido: GitHub authentication`. If a runtime-specific adapter is required, use repo-local instructions and mark support as validation pending until the target runtime is observed.

## Validation

- Evidence grounded: yes.
- Unsupported capabilities marked pending: yes.
- Local-first fallback present: yes.
- Offline contract: `skills/runtime-routing/scripts/check.sh`.
