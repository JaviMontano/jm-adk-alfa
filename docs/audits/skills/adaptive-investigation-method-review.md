# adaptive-investigation-method review

## Verdict

`adaptive-investigation-method` is DoD-ready in this prepared patch. It has concrete assets, deterministic scripts, fixtures, eval cases, examples, knowledge files, and a ledger update.

## Evidence

- `skills/adaptive-investigation-method/assets/` defines the investigation schema, loop policy, report template, and manifest.
- `skills/adaptive-investigation-method/scripts/compile-adaptive-investigation.py` validates bounded investigation-loop specs and renders deterministic Markdown or JSON reports.
- `skills/adaptive-investigation-method/scripts/check.sh` validates valid repo/corpus investigations and rejects missing-budget and reflexive-replan cases.
- `skills/adaptive-investigation-method/evals/evals.json` contains activation, compiler, negative fixture, conflict, and false-positive cases.

## Gates

- `bash skills/adaptive-investigation-method/scripts/check.sh` -> PASS (`OK: adaptive-investigation-method scripts are deterministic`).
- `python3 -B scripts/validate-skill-dod.py --skill adaptive-investigation-method` -> PASS (`skill=adaptive-investigation-method dod=pass errors=0`).
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill adaptive-investigation-method` -> PASS (`skills_with_scripts=1 warnings=0 errors=0`).
- `audit_skill_dod_state.py --repo . --skill adaptive-investigation-method --run-check` -> PASS (`status=pass`, `missing=[]`).
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks` -> PASS (`skills_with_scripts=54 warnings=0 errors=0`).
- `python3 -B scripts/validate-skills.py --strict` -> PASS (`skills=585 warnings=0 errors=0`).
- `python3 -B scripts/count-components.py --check-docs` -> PASS (`skills=585 agents=260 commands=267 prompts=256 components=1368`).
- `bash scripts/check-repo-boundaries.sh` -> PASS (`Repo boundaries OK`).
- `python3 -B scripts/qa/run-adversarial-tests.py` -> PASS (`passed=11 failed=0 total=11`).
- `bash -n skills/adaptive-investigation-method/scripts/check.sh` -> PASS.
- `PYTHONPYCACHEPREFIX=<tmp>/pycache python3 -m py_compile skills/adaptive-investigation-method/scripts/compile-adaptive-investigation.py` -> PASS.
- `git diff --check` -> PASS.

## Limits

- The compiler validates the investigation plan structure; it does not inspect a real target repo or corpus.
- Quality still depends on accurate evidence captured in the user-provided investigation spec.
- The script blocks known anti-pattern tokens and invalid replan triggers, but it cannot prove every possible investigation strategy is optimal.

## Ledger Completion 2026-06-05

- [CODE] `bash skills/adaptive-investigation-method/scripts/check.sh` passed in `codex/complete-script-backed-ledger-20260605` validation.
- [CODE] `python3 -B scripts/validate-skill-dod.py --skill adaptive-investigation-method` passed with `skill=adaptive-investigation-method dod=pass errors=0`.
- [CODE] `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill adaptive-investigation-method` passed with `skills_with_scripts=1 warnings=0 errors=0`.
- [CONFIG] `docs/audits/skill-review-ledger.csv` now records `adaptive-investigation-method` as `dod-complete`.
