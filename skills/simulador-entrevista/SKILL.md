---
name: simulador-entrevista
version: 0.2.0
description: "This skill should be used when the user asks to run a mock interview, practice one interview question at a time, score an answer across separate substance, English, and presence rubrics, choose the next practice step, or validate interview feedback without averaging the dimensions."
owner: "JM Labs"
triggers:
  - simulador-entrevista
  - interview-sim
  - mock-interview
  - practice interview
  - interview feedback
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# Simulador Entrevista

## Purpose

Run deterministic mock-interview practice one question at a time. Ask or evaluate exactly one question per turn, keep three rubrics separate (`substance`, `english`, `presence`), require evidence snippets for each score, and produce one next practice step based on the weakest dimension.

Use this skill for practice and feedback, not for guaranteeing interview success, fabricating candidate stories, or replacing human hiring judgment.

## Deterministic Contract

Follow `assets/output-contract.json` and validate reports with `scripts/interview_sim_validator.py`. A valid report must include:

- A session object with role, language (`es` or `en`), turn number, and `one_question_mode=true`.
- One question from `scripts/question_bank.json` or a supplied question with a stable ID.
- A concise answer summary and evidence snippets from the provided answer.
- Separate rubric objects for `substance`, `english`, and `presence`.
- Scores from 1 to 5 with evidence reference and rationale per dimension.
- No `overall_score`, no averaging, and no collapsed verdict.
- Exactly one next step targeting the weakest dimension by stable order: `substance`, then `english`, then `presence`.

## Workflow

1. Select one question from `scripts/question_bank.json` by role, language, and angle. If the user supplies a question, assign a stable `Q-CUSTOM-001` ID.
2. Ask only that question and wait for the answer unless the user already supplied an answer.
3. Summarize the answer without inventing facts.
4. Score the answer on the three separate rubrics in `assets/rubric-policy.json`.
5. Attach at least one evidence snippet to each rubric score.
6. Block when any score is below the floor in `assets/feedback-policy.json`, when the report uses an average, or when it promises success.
7. Validate the JSON report with `scripts/interview_sim_validator.py`.
8. Produce the markdown handoff from `templates/output.md`.

## Output Rules

- Tag claims with `[EXPLICIT]`, `[INFERRED]`, or `[OPEN]`.
- Keep feedback actionable and bounded to the submitted answer.
- Do not infer work history, achievements, English fluency, personality, seniority, or hiring outcome beyond the answer.
- Do not provide a script for lying or fabricating experience.
- Do not ask multiple questions in the same turn.

## Assets

- `assets/manifest.json` lists deterministic assets.
- `assets/output-contract.json` defines the report structure.
- `assets/rubric-policy.json` defines the three separate rubrics and score ranges.
- `assets/question-policy.json` defines one-question mode and question IDs.
- `assets/feedback-policy.json` defines floor, flags, and next-step selection.
- `assets/safety-policy.json` defines success-promise and fabrication blockers.

## Scripts

Run:

```bash
python3 skills/simulador-entrevista/scripts/interview_sim_validator.py --input <report.json>
bash skills/simulador-entrevista/scripts/check.sh
```

The validator is offline and rejects missing evidence, invalid score ranges, low-floor scores, average/overall scores, multiple-question turns, unresolved next steps, unsupported language, and guaranteed-outcome language.

## Related Skills

- `proceso-seleccion-orchestrator`
- `red-y-referencias`
- `gratitud-post-proceso`

## Stop Conditions

Stop when the user asks for guaranteed success, fabricated experience, deception, or evaluation based on unstated private data. Ask for the answer text before scoring when no answer is supplied.
