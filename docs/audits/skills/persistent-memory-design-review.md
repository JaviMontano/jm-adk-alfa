# persistent-memory-design Review

Date: 2026-06-06
Branch: `codex/harden-persistent-memory-design-dod-20260606`
Status: dod-complete; local validation passed

## Scope

- Allowed: `skills/persistent-memory-design/**`
- Allowed: `docs/audits/skills/persistent-memory-design-review.md`
- Allowed after full local validation: the `persistent-memory-design` row in `docs/audits/skill-review-ledger.csv`
- Forbidden: other skills, shared validators, CI, unrelated docs, or cross-skill edits

## SpokeReport - Determinism Auditor

status: warn

findings:
- The skill content is domain-specific and already covers persistent scratchpads, fixed sections, evidence, read-once access, compact survival, and anti-patterns.
- DoD failed before hardening because `assets/` was missing and eval expected checks did not include `assets` or `deterministic_scripts`.

coverage_gaps:
- No deterministic asset contract for safe path, fixed sections, evidence, read policy, write policy, compact recovery, or report shape.
- No offline validator to reject raw transcripts, unsafe paths, re-read-per-turn designs, full rewrites, schema drift, missing evidence, or conversation dependency.

recommended_changes:
- Add deterministic assets and manifest.
- Add script fixtures and validator.
- Harden eval expected checks.

risk:
- Without offline validation, a report could claim durable memory while still relying on volatile conversation state or cache-breaking repeated reads.

## SpokeReport - Eval Designer

status: warn

findings:
- Evals already include activation, false positives, empty input, and conflicting requirements.
- Expected checks were too narrow for the current DoD gate.

coverage_gaps:
- Missing explicit assets/scripts checks.
- Missing deterministic checks for unsafe path, evidence gaps, raw transcript dumps, schema drift, and re-read behavior.

recommended_changes:
- Add `assets`, `deterministic_scripts`, `quality_criteria`, and evidence/read/write/recovery checks to eval cases.
- Back the cases with offline fixtures.

risk:
- Activation could be correct while the output contract remains unverifiable.

## SpokeReport - Script Engineer

status: pass

findings:
- A local validator adds real deterministic coverage because the expected report is structured JSON and can be checked without network, time, random values, or repository mutation.

coverage_gaps:
- None after adding valid and negative fixtures for the report contract.

recommended_changes:
- Run `bash skills/persistent-memory-design/scripts/check.sh` in local and CI-style validation.

risk:
- Residual risk is limited to markdown-only outputs not converted into the JSON report contract.

## HardeningBrief

skill: `persistent-memory-design`

scope_allowed:
- `skills/persistent-memory-design/**`
- `docs/audits/skills/persistent-memory-design-review.md`
- `docs/audits/skill-review-ledger.csv` row for `persistent-memory-design`

required_changes:
- Deterministic assets and `assets/manifest.json`.
- Offline report validator and fixtures.
- Hardened eval expected checks.
- Review doc and ledger evidence after validation.

forbidden_changes:
- Other skills.
- Shared validators.
- Repo workflow or CI files.
- Unrelated ledger rows.

validation_plan:
- `bash skills/persistent-memory-design/scripts/check.sh`
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill persistent-memory-design`
- `python3 -B scripts/validate-skill-dod.py --skill persistent-memory-design`
- Repo validation suite before PR.

merge_criteria:
- Per-skill validation passes.
- Repo validation passes.
- PR Quality Gates pass.
- Squash merge completes and branch cleanup succeeds.

## Evidence

Per-skill validation:
- `bash skills/persistent-memory-design/scripts/check.sh`: passed; 2 valid fixtures accepted and 7 invalid fixtures rejected.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill persistent-memory-design`: passed with `skills_with_scripts=1 warnings=0 errors=0`.
- `python3 -B scripts/validate-skill-dod.py --skill persistent-memory-design`: passed with `dod=pass errors=0`.

Repo validation:
- `python3 -B scripts/validate-skills.py --strict`: passed with `skills=600 warnings=0 errors=0`.
- `python3 -B scripts/count-components.py --check-docs`: passed with `skills=600 agents=261 commands=267 prompts=256 components=1384`.
- `bash scripts/check-repo-boundaries.sh`: passed with `Repo boundaries OK`.
- `python3 -B scripts/qa/run-adversarial-tests.py`: passed with `summary: passed=11 failed=0 total=11`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks`: passed with `skills_with_scripts=67 warnings=0 errors=0`.
- `bash scripts/doc-factory/check.sh`: passed with deterministic smoke check.
- `git diff --check`: passed.

## Guardian Decision

Pass. Per-skill and repo validation are green, scope is confined to the active skill, the review doc exists, and the ledger row may be marked `dod-complete`.
