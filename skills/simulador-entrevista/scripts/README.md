# Scripts

## interview_sim_validator.py

Validates a deterministic mock-interview feedback report. It checks one-question mode, question ID, language, evidence snippets, separate rubric scores, score ranges, no average/overall score, weakest-dimension next step, and safety blockers.

```bash
python3 skills/simulador-entrevista/scripts/interview_sim_validator.py --input skills/simulador-entrevista/scripts/fixtures/valid-english-feedback.json
```

## check.sh

Runs valid, blocked, and invalid fixtures offline. Expected result: valid fixtures exit `0`; blocked and invalid fixtures exit non-zero.
