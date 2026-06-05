# Auto Prompt Matching Primary Prompt

## Objective

Route the user's request to the best source-backed skill or prompt without executing the downstream task.

## Required Inputs

- Raw user request
- Explicit prefix or command, if present
- Available routing sources
- Constraints, brand, artifact type, and requested language

## Process

1. Inspect explicit prefix/command, `PRISTINO-INDEX.md`, `.agent/skills_index.json`, matching `skills/*/SKILL.md`, and prompt metadata.
2. Build a candidate list only from discovered sources.
3. Score candidates with `assets/routing-checklist.md`.
4. Apply stable tie-breakers.
5. Return `route`, `ask`, or `decline`.
6. Validate that no downstream task was executed.

## Output

Return a Markdown routing packet with selected route, confidence band, candidate scores, source evidence, rejected alternatives, coverage gaps, and next action.
