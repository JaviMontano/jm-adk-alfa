# X-Ray Skill -- Body of Knowledge

## Canon

`x-ray-skill` is a read-only skill-quality diagnostic. It inspects the structure and text of a target skill, then reports certification readiness with evidence.

## Core Objects

- Skill directory: root folder that must contain one top-level `SKILL.md`.
- Rubric score: one of 10 dimensions scored from 1 to 10.
- Gate result: one of 13 binary checkpoints.
- Certification readiness: `CERTIFIED`, `CONDITIONAL`, or `BLOCKED`.
- Component classification: status of `SKILL.md`, `references/`, `scripts/`, `agents/`, `evals/`, `assets/`, examples, templates, and prompts.

## Deterministic Signals

| Signal | Good State | Failure State |
|---|---|---|
| Frontmatter | `name` and trigger-rich `description` parse cleanly | Missing or malformed routing metadata |
| Body structure | Usage, process, limits, edge cases, examples, and gate present | Generic scaffold sections or missing calibration |
| References | All paths mentioned in SKILL.md resolve | Broken or orphan references |
| Evals | Distinct happy, edge, and false-positive cases | Repeated generic activation cases |
| Scripts | Read-only compiler and fixture checks pass | No deterministic subset for repeated scoring |

## Limits

Structural quality is not runtime quality. A skill can pass X-Ray and still need behavioral evals for domain correctness.
