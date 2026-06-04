# x-ray-skill review

## Verdict

`x-ray-skill` is DoD-ready in this prepared patch. It has concrete assets, deterministic scripts, fixtures, eval cases, examples, knowledge files, and a ledger update.

## Evidence

- `skills/x-ray-skill/assets/` defines the rubric policy, gate policy, report template, and manifest.
- `skills/x-ray-skill/scripts/compile-x-ray-report.py` validates real skill directories or virtual fixtures and renders deterministic Markdown or JSON scorecards.
- `skills/x-ray-skill/scripts/check.sh` validates certified, draft, missing-SKILL, and self-audit cases.
- `skills/x-ray-skill/evals/evals.json` contains activation, compiler, certified fixture, blocked fixture, fail-closed, archive, large-skill, and false-positive cases.

## Gates

- `bash skills/x-ray-skill/scripts/check.sh` -> PASS (`OK: x-ray-skill scripts are deterministic`).
- `python3 -B scripts/validate-skill-dod.py --skill x-ray-skill` -> PASS (`skill=x-ray-skill dod=pass errors=0`).
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill x-ray-skill` -> PASS (`skills_with_scripts=1 warnings=0 errors=0`).
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks` -> PASS (`skills_with_scripts=52 warnings=0 errors=0`).
- `python3 -B scripts/validate-skills.py --strict` -> PASS (`skills=585 warnings=0 errors=0`).
- `python3 -B scripts/count-components.py --check-docs` -> PASS (`skills=585 agents=260 commands=267 prompts=256 components=1368`).
- `bash scripts/check-repo-boundaries.sh` -> PASS (`Repo boundaries OK`).
- `python3 -B scripts/qa/run-adversarial-tests.py` -> PASS (`passed=11 failed=0 total=11`).
- `bash -n skills/x-ray-skill/scripts/check.sh` -> PASS.
- `PYTHONPYCACHEPREFIX=<tmp>/pycache python3 -m py_compile skills/x-ray-skill/scripts/compile-x-ray-report.py` -> PASS.
- `git diff --check` -> PASS.
- `audit_skill_dod_state.py --repo . --skill x-ray-skill --run-check` -> PASS (`status=pass`, `missing=[]`).

## Limits

- The compiler evaluates structural quality; it does not prove runtime behavior of the target skill.
- Large-skill deep review may still require manual sampling after deterministic scoring.
- The script is read-only and never modifies the audited skill.
