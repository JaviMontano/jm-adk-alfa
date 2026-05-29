# Local Pattern Inventory

## Summary

This audit records local patterns reviewed for Alfa's first-use, context, memory, task handling, prompting, scripting, and multi-runtime evolution. It does not import local documents wholesale.

## Inventory

| Source | Type | Observed Signal | Decision | Owner Artifact |
|---|---|---|---|---|
| Alfa `commands/onboarding.md` | command | Existing onboarding had stale `101` counts and project-build flow | adapt | `commands/onboarding.md`, `commands/first-use.md` |
| Alfa `skills/session-start-bootstrap` | skill | Context loading and guardrails initialization | adapt | `docs/FIRST_USE_ONBOARDING.md` |
| Alfa `skills/context-window-management` | skill | Token budgeting and context compression | adapt | `docs/PROMPTING.md`, `skills/runtime-routing` |
| Alfa `scripts/workspace-manager.sh` | script | Workspace registry, tasklog, changelog, plan | adapt | `docs/WORKSPACE_SETUP.md`, `scripts/setup-workspace-profile.py` |
| Alfa `scripts/adapters/codex.sh` | adapter | Generates Codex/Gemini runtime docs | adapt | `AGENTS.md`, `GEMINI.md`, `CODEX.md` |
| Alfa `scripts/adapters/antigravity.sh` | adapter | Generates `.agent/` derived view | adapt | `ANTIGRAVITY.md`, `.agent/rules/GEMINI.md` |
| Local Jarvis playbook/runbook | playbook/runbook | Portable context, memory audit, prompt-first setup, provider portability | adapt | docs and skills |
| Local Codex UX snapshots | process evidence | Runtime choice and setup UX signals | discard runtime | this audit |
| Local Antigravity semantic nodes | generated tool notes | Antigravity marked as tool to verify when source is insufficient | backlog/adapt | `ANTIGRAVITY.md` |
| Local dataless Antigravity prompt placeholder | degraded source | Source was not materialized | discard | no runtime import |

## Durable Rules Adopted

| Pattern | Decision | Destination | Eval or Check |
|---|---|---|---|
| Confirm repo before editing | adopt | `workspace-diagnostic-agent`, `diagnose-first-use.py` | `ONBOARDING-004` |
| Greeting starts guided setup | add | `first-use-onboarding-agent`, `first-use-onboarding` | `ONBOARDING-001` |
| Explicit task is not blocked by onboarding | add | `task-intake-agent` | `ONBOARDING-003` |
| Local profile is gitignored state | adopt | `setup-workspace-profile.py` | `FIRST-USE-SCRIPT-002` |
| Prompt behavior needs evals | adapt | `docs/EVALS.md`, `evals/onboarding/evals.json` | `validate-onboarding.py` |
| Runtime claims require evidence | adapt | `runtime-routing-agent`, `ANTIGRAVITY.md`, `CODEX.md` | readiness check |
| Process evidence is not runtime canon | adopt | `docs/ARCHIVE_POLICY.md` | no-regression checklist |

## Backlog

- Validate Antigravity behavior in a real Antigravity runtime.
- Add VS Code-specific generated adapter only after repo evidence or runtime requirements are defined.
- Add memory persistence adapters only when target runtimes expose confirmed storage or file-loading behavior.
