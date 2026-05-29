---
description: "Intake the first concrete task after onboarding and create only the minimum safe working context."
user-invocable: true
---

# /jm-adk:start-task

## Purpose

Move from guided setup to execution without over-asking.

## Workflow

1. Classify the input as explicit task, vague intent, continuation, or topic change.
2. Ask only for blocking missing information.
3. If artifact-producing work starts, derive a workspace slug and use the workspace manager according to `CLAUDE.md`.
4. Preserve local profile and workspace boundaries.

## Agent

Use `task-intake-agent`.
