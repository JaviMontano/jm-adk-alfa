---
description: "Compatibility entrypoint for the Alfa first-use onboarding flow."
user-invocable: true
---

# /jm-adk:onboarding

## Purpose

Compatibility command for users who know the older onboarding command. Route to `/jm-adk:first-use` and use the current component counts from `python3 scripts/count-components.py`.

## Workflow

1. Run `python3 scripts/diagnose-first-use.py --dry-run`.
2. If the status is `requires_confirmation`, stop with `Dato requerido`.
3. If the user provided only a greeting or no concrete task, activate `first-use-onboarding-agent`.
4. If the user provided an explicit task, activate `task-intake-agent` for minimal missing context and continue.
5. If local profile setup is requested, use `/jm-adk:setup-workspace`.

## Related Commands

- `/jm-adk:first-use`
- `/jm-adk:diagnose-workspace`
- `/jm-adk:setup-workspace`
- `/jm-adk:start-task`
