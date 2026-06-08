# Safe Scripting And Bash Review

## SpokeReport - Determinism Auditor

- status: pass
- findings: Initial DoD failed because `assets/` was missing, scaffold text remained in knowledge and examples, and evals did not require deterministic scripts or assets.
- coverage_gaps: Write surface, dry-run default, explicit apply/force, destructive pattern guard, portability, offline validation, and Guardian consistency were not machine-checkable.
- recommended_changes: Add deterministic assets, specialized evals, offline validator, fixtures, review doc, and ledger reconciliation after validation.
- risk: Without structural checks, a reusable script can mutate files, expose secrets, or rely on user-specific paths while appearing safe in prose.

## SpokeReport - Eval Designer

- status: pass
- findings: Replaced generic evals with deterministic cases covering dry-run script design, explicit review trigger, minimal input, broad writes, false positive, empty input, destructive command request, secret exposure, network dependency, upgrade safety, and tempdir portability.
- coverage_gaps: None remaining for this DoD hardening scope.
- recommended_changes: Keep evals tied to `assets`, `deterministic_scripts`, `dry_run_default`, `write_surface`, `destructive_guard`, `portability`, and `offline_validation`.
- risk: Future eval edits could normalize dangerous shell patterns as long as they are wrapped in friendly prose.

## SpokeReport - Script Engineer

- status: pass
- findings: Added `scripts/validate_safe_scripting_and_bash.py`, `scripts/check.sh`, 2 valid fixtures, and 10 invalid mutation fixtures.
- coverage_gaps: The script validates JSON script-safety reports; individual production scripts still need their own `bash -n` and smoke tests.
- recommended_changes: Use the JSON contract before approving reusable scripts that write, sync, delete, or overwrite local files.
- risk: Shell behavior varies by platform; production scripts must still avoid GNU-only assumptions or guard them explicitly.

## HardeningBrief

- skill: safe-scripting-and-bash
- scope_allowed: `skills/safe-scripting-and-bash/**`, `docs/audits/skills/safe-scripting-and-bash-review.md`, and the `safe-scripting-and-bash` ledger row.
- required_changes: Assets, eval cases, README/SKILL updates, offline scripts, fixtures, review doc, and ledger update after validation.
- forbidden_changes: Other skills, repo-level validators, unrelated docs, or unrelated ledger rows.
- validation_plan: Skill DoD, skill script contract, local check script, repo strict validation, docs count, repo boundaries, adversarial tests, doc-factory check, global script checks, and diff whitespace check.
- merge_criteria: Local validation green, PR ready, Quality Gates green, squash merge, branch cleanup, and updated `main`.

## Local Evidence

- `bash skills/safe-scripting-and-bash/scripts/check.sh`: `safe-scripting-and-bash check passed: valid=2 invalid=10`.
- `python3 -B scripts/validate-skill-dod.py --skill safe-scripting-and-bash`: `skill=safe-scripting-and-bash dod=pass errors=0`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill safe-scripting-and-bash`: `skills_with_scripts=1 warnings=0 errors=0`.
- `python3 -B scripts/validate-skills.py --strict`: `skills=600 warnings=0 errors=0`.
- `python3 -B scripts/count-components.py --check-docs`: `skills=600 agents=261 commands=267 prompts=256 components=1384`.
- `bash scripts/check-repo-boundaries.sh`: `Repo boundaries OK`.
- `python3 -B scripts/qa/run-adversarial-tests.py`: `summary: passed=11 failed=0 total=11`.
- `bash scripts/doc-factory/check.sh`: `OK: doc-factory deterministic smoke check passed`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks`: `skills_with_scripts=117 warnings=0 errors=0`.
- `git diff --check`: pass with no output.

## Guardian Decision

- status: pass
- decision: Authorize PR creation because the skill now has deterministic assets, evals, offline scripts, fixtures, review doc, reconciled ledger row, and passing local validation evidence.
- remaining_risks: Production shell scripts still need direct syntax and smoke tests in their own repository context.
