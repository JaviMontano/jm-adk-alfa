# katas-session-resume-fork Review

Date: 2026-06-06
Branch: `codex/harden-katas-session-resume-fork-dod-20260606`
Status: dod-complete; local validation passed

## Scope

- Allowed: `skills/katas-session-resume-fork/**`
- Allowed: `docs/audits/skills/katas-session-resume-fork-review.md`
- Allowed after full local validation: the `katas-session-resume-fork` row in `docs/audits/skill-review-ledger.csv`
- Forbidden: other skills, shared validators, CI, unrelated docs, or cross-skill edits

## SpokeReport - Determinism Auditor

status: warn

findings:
- `SKILL.md`, agents, prompts, template, and knowledge already describe the Kata 25 domain: resume, fork, fresh, stale tool results, and typed summaries.
- DoD failed before hardening because assets were missing, examples were scaffold-generic, evals were generic, and no deterministic script existed.

coverage_gaps:
- No assetized decision matrix for `resume|fork|fresh`.
- No offline validator for stale-result rejection, fork isolation, typed-summary requirements, raw transcript rejection, or command/decision alignment.

recommended_changes:
- Add deterministic assets and manifest.
- Replace scaffold examples and evals with domain cases.
- Add an offline JSON validator with valid and negative fixtures.

risk:
- Without validation, the kata could approve `--resume` after a refactor or inject an old transcript into a fresh session.

## SpokeReport - Eval Designer

status: block

findings:
- Existing evals included generic `happy_path`, generic explicit trigger, and scaffold-style upgrade/local cases.
- The DoD rejected generic eval inputs.

coverage_gaps:
- Missing realistic resume/fork/fresh cases.
- Missing false positives, false negatives, conflicts, degradation, and boundary checks.

recommended_changes:
- Replace evals with deterministic scenarios covering valid resume, fork, fresh after refactor, synonym activation, unrelated false positive, empty input, stale conflict, insufficient input, and missing scratchpad degradation.

risk:
- Generic evals do not prove the kata's routing or output quality.

## SpokeReport - Script Engineer

status: pass

findings:
- The expected report can be represented as JSON with `decision`, `signals`, `command`, optional `summary`/`fork`, and `validation` fields.
- A local validator can check this contract without network, time, random values, or mutation.

coverage_gaps:
- None after adding fixtures for valid resume/fork/fresh and six negative cases.

recommended_changes:
- Run `bash skills/katas-session-resume-fork/scripts/check.sh` before PR.

risk:
- Residual risk is limited to markdown-only outputs not converted into the JSON report contract.

## HardeningBrief

skill: `katas-session-resume-fork`

scope_allowed:
- `skills/katas-session-resume-fork/**`
- `docs/audits/skills/katas-session-resume-fork-review.md`
- `docs/audits/skill-review-ledger.csv` row for `katas-session-resume-fork`

required_changes:
- Deterministic assets and `assets/manifest.json`.
- Domain-specific examples and evals.
- Offline report validator and fixtures.
- Review doc and ledger evidence after validation.

forbidden_changes:
- Other skills.
- Shared validators.
- Repo workflow or CI files.
- Unrelated ledger rows.

validation_plan:
- `bash skills/katas-session-resume-fork/scripts/check.sh`
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill katas-session-resume-fork`
- `python3 -B scripts/validate-skill-dod.py --skill katas-session-resume-fork`
- Repo validation suite before PR.

merge_criteria:
- Per-skill validation passes.
- Repo validation passes.
- PR Quality Gates pass.
- Squash merge completes and branch cleanup succeeds.

## Evidence

Per-skill validation:
- `bash skills/katas-session-resume-fork/scripts/check.sh`: passed; 3 valid fixtures accepted and 6 invalid fixtures rejected.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill katas-session-resume-fork`: passed with `skills_with_scripts=1 warnings=0 errors=0`.
- `python3 -B scripts/validate-skill-dod.py --skill katas-session-resume-fork`: passed with `dod=pass errors=0`.

Repo validation:
- `python3 -B scripts/validate-skills.py --strict`: passed with `skills=600 warnings=0 errors=0`.
- `python3 -B scripts/count-components.py --check-docs`: passed with `skills=600 agents=261 commands=267 prompts=256 components=1384`.
- `bash scripts/check-repo-boundaries.sh`: passed with `Repo boundaries OK`.
- `python3 -B scripts/qa/run-adversarial-tests.py`: passed with `summary: passed=11 failed=0 total=11`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks`: passed with `skills_with_scripts=68 warnings=0 errors=0`.
- `bash scripts/doc-factory/check.sh`: passed with deterministic smoke check.
- `git diff --check`: passed.

## Guardian Decision

Pass. Per-skill and repo validation are green, scope is confined to the active skill, the review doc exists, and the ledger row may be marked `dod-complete`.
