# workflow-orchestration review

## Verdict

`workflow-orchestration` is DoD-ready in this prepared patch. It has concrete assets, deterministic scripts, fixtures, eval cases, examples, knowledge files, and review evidence. The ledger CSV is intentionally deferred from this PR.

## Evidence

- `skills/workflow-orchestration/assets/` defines orchestration schema, checkpoint policy, resume policy, and report template.
- `skills/workflow-orchestration/scripts/compile-orchestration-plan.py` validates structured JSON and renders deterministic Markdown.
- `skills/workflow-orchestration/scripts/check.sh` validates product launch, incident recovery, and invalid missing-resume fixtures.
- `skills/workflow-orchestration/evals/evals.json` contains activation, false-positive, resume, checkpoint, observability, vague-action, and compiler cases.

## Gates

- `bash skills/workflow-orchestration/scripts/check.sh` -> PASS (`OK: workflow-orchestration scripts are deterministic`).
- `python3 -B scripts/validate-skill-dod.py --skill workflow-orchestration` -> PASS (`skill=workflow-orchestration dod=pass errors=0`).
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill workflow-orchestration` -> PASS (`skills_with_scripts=1 warnings=0 errors=0`).
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks` -> PASS (`skills_with_scripts=20 warnings=0 errors=0`).
- `python3 -B scripts/validate-skills.py --strict` -> PASS (`skills=585 warnings=0 errors=0`).
- `python3 -B scripts/count-components.py --check-docs` -> PASS (`skills=585 agents=260 commands=267 prompts=256 components=1368`).
- `bash scripts/check-repo-boundaries.sh` -> PASS (`Repo boundaries OK`).
- `python3 -B scripts/qa/run-adversarial-tests.py` -> PASS (`summary: passed=11 failed=0 total=11`).
- `git diff --check` -> PASS.
- `audit_skill_dod_state.py --repo . --skill workflow-orchestration --run-check` -> PASS (`status=pass`, `missing=[]`).

## Limits

- The compiler validates orchestration structure offline; it does not execute external workflow steps.
- Resume state paths are validated for specificity, not for runtime existence.
- Live orchestration still requires the caller to persist the rendered checkpoint log in the active workspace.
