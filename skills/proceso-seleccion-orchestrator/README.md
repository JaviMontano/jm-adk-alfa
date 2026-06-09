# proceso-seleccion-orchestrator

Deterministic orchestration for selection-process tracking. The skill converts supplied email snippets, recruiter notes, interview notes, or manual entries into a verifiable status board with evidence IDs, interview stages, contacts, risks, and exactly one next action.

## Offline Validation

```bash
bash skills/proceso-seleccion-orchestrator/scripts/check.sh
python3 -B scripts/validate-skill-dod.py --skill proceso-seleccion-orchestrator
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill proceso-seleccion-orchestrator
```

## Determinism Rules

- Accept only supplied evidence; never query mail, calendars, web, or applicant systems by default.
- Require ISO `YYYY-MM-DD` dates; relative dates create blockers.
- Require stable evidence references for stages, contacts, risks, and next action.
- Reject guaranteed hiring or rejection language unless it is quoted as evidence and marked as a risk.
- Validate JSON reports with `scripts/selection_board_validator.py` before handoff.
