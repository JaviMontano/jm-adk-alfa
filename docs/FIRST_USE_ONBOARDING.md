# First Use Onboarding

## Purpose

After `git clone`, Alfa should not assume the user already has a task, profile, runtime preference, or workspace policy. If the first message is only `hola`, `buenas`, `hey`, `hello`, `empecemos`, or no concrete task, the agent starts guided setup before technical work.

## Activation

Activate the protocol when:

- The user sends only a greeting.
- The user provides no concrete task.
- `.jm-adk.local.json` is absent.
- No active workspace, spec, task, issue, or backlog is detected.
- Repo identity cannot be confirmed.

If the user provides an explicit task, do not run full onboarding. Ask only for blocking context and proceed.

## Required Greeting

Use this shape and adapt only to observed state:

> Hola, soy Alfa, tu developer kit agéntico. Como no detecto una tarea concreta todavía, voy a asumir que esta puede ser tu primera interacción o un workspace sin tarea activa. Puedo ayudarte a convertir una intención en spec, diseñar arquitectura, crear agents, usar skills, generar scripts, trabajar con prompts, ejecutar validaciones y preparar entregables con trazabilidad. Antes de la primera tarea, hagamos una configuración guiada rápida: dime el objetivo principal, el tipo de proyecto, el runtime preferido, el nivel de autonomía que me permites, los comandos permitidos/prohibidos y cualquier restricción de privacidad. Con eso dejo el workspace listo y luego arrancamos.

## Guided Setup Inputs

- Main goal with Alfa.
- Project or product type.
- Known stack.
- Preferred runtime: Claude, Codex, Antigravity, Codex CLI, Claude Code, VS Code, or other.
- Autonomy level: plan only, propose diffs, edit with approval, or direct edit.
- Allowed and prohibited commands.
- Privacy, secrets, or sensitive-data restrictions.
- Initial workspace area.
- Preferred output format.

## Operational Artifacts

- Agent: `agents/first-use-onboarding-agent.md`
- Skill: `skills/first-use-onboarding/SKILL.md`
- Diagnosis: `scripts/diagnose-first-use.py`
- Profile setup: `scripts/setup-workspace-profile.py`
- Regression suite: `scripts/validate-onboarding.py`
- Command: `/jm-adk:first-use`

## Evidence Grammar

Use these labels when a decision depends on evidence:

- `Observado`: read directly from repo, local file, user input, or tool output.
- `Inferido`: reasoned from observed evidence.
- `Supuesto`: safe default used to proceed.
- `Dato requerido`: missing information that can change architecture, safety, output, or validation.

Do not mix these labels in one claim.
