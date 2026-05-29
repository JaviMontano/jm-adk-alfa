# Prompting

## Purpose

Alfa prompts should turn intent into executable instructions with clear scope, output shape, and validation.

## Prompt Contract

A durable prompt includes:

- Role.
- Situation or context.
- Task.
- Execution sequence.
- Constraints and safety boundaries.
- Output shape.
- Acceptance criteria.
- Edge cases.

## Rules

- Prefer portable Markdown prompts unless the runtime requires a specific format.
- Put critical context at the beginning or end; do not bury it in the middle.
- Mark missing facts as `Dato requerido` or validation pending.
- Add eval cases when prompt behavior changes.
- Do not expose hidden reasoning; ask for concise rationale or evidence instead.

## Related Skill

Use `skills/prompting-and-meta-prompting/SKILL.md` for reusable prompt design and review.
