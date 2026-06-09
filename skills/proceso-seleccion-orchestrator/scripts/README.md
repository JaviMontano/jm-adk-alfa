# Scripts

## selection_board_validator.py

Validates a deterministic selection-process board JSON file. It checks schema, skill slug, candidate fields, evidence references, ISO dates, status policy, risk policy, duplicate stages, one next action, and blocker language.

```bash
python3 skills/proceso-seleccion-orchestrator/scripts/selection_board_validator.py --input skills/proceso-seleccion-orchestrator/scripts/fixtures/valid-selection-board.json
```

## check.sh

Runs valid, blocked, and invalid fixtures offline. Expected result: valid fixtures exit `0`; blocked and invalid fixtures exit non-zero.
