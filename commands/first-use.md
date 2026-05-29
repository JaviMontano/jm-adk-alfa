---
description: "Start Alfa first-use onboarding after clone, greeting-only input, or missing task context."
user-invocable: true
---

# /jm-adk:first-use

## Purpose

Run the guided Alfa first-use flow before the first technical task.

## Workflow

1. Run `python3 scripts/diagnose-first-use.py --dry-run --input "<user input>"`.
2. If Alfa is not confirmed, report `Dato requerido` and do not edit.
3. If the input is a greeting or empty, present Alfa, explain the developer kit, and request the minimum setup inputs in one round.
4. If the user asks to create local profile state, route to `/jm-adk:setup-workspace`.
5. Ask for the first concrete task after setup.

## Agents And Skills

- Agent: `first-use-onboarding-agent`
- Skill: `first-use-onboarding`
- Support: `workspace-diagnostic-agent`, `task-intake-agent`
