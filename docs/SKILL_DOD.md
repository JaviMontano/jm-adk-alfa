# Skill Definition of Done

This DoD is applied one skill at a time.

## Required Evidence

- Canonical scaffold files pass `python3 scripts/validate-skills.py --strict`.
- The selected skill passes `python3 scripts/validate-skill-dod.py --skill <skill>`.
- If the skill has `scripts/`, it passes `python3 scripts/validate-skill-scripts.py --strict --run-checks --skill <skill>`.
- The skill has `assets/README.md` and `assets/manifest.json`.
- Every manifest asset exists, has a purpose, has a type, and declares `used_by` targets.
- `SKILL.md` references `assets/` and any deterministic script entry points.
- Examples, evals, and body-of-knowledge are skill-specific and do not retain generic scaffold text.
- The review result is recorded in `docs/audits/skill-review-ledger.csv`.

## Completion Status

A skill is complete only when every item above is proven by command output or file inspection.
