# input-analysis Review

Date: 2026-06-06
Branch: `codex/harden-input-analysis-dod-20260606`
Status: dod-complete; local validation passed

## Scope

- Allowed: `skills/input-analysis/**`
- Allowed: `docs/audits/skills/input-analysis-review.md`
- Allowed after full local validation: the `input-analysis` row in `docs/audits/skill-review-ledger.csv`
- Forbidden: other skills, shared validators, CI, unrelated docs, or cross-skill edits

## SpokeReport - Determinism Auditor

status: block

findings:
- `SKILL.md` defines evidence-tagged input analysis, contradiction/gap/ambiguity detection, completeness scoring, Firebase feasibility, and assumption warnings.
- DoD failed before hardening because assets were missing, examples were scaffold-generic, and evals were a legacy array without `cases`.

coverage_gaps:
- No deterministic asset contract for evidence tags, finding taxonomy, completeness scoring, assumption warnings, or report shape.
- No offline validator for missing evidence tags, out-of-range scores, missing assumption warning, implementation leakage, or missing actions.

recommended_changes:
- Add deterministic assets and manifest.
- Replace scaffold examples and legacy evals.
- Add an offline JSON validator with valid and negative fixtures.

risk:
- Without validation, an input analysis report could ship untagged findings, arbitrary scores, or implementation details inside analysis.

## SpokeReport - Eval Designer

status: block

findings:
- Existing evals were not in the DoD `cases` object format.
- Existing examples retained scaffold markers rejected by the DoD.

coverage_gaps:
- Missing realistic RFP/brief/email cases.
- Missing false positives, contradiction cases, ambiguity cases, assumption-heavy degradation, and phase-separation boundary.

recommended_changes:
- Replace evals with deterministic `cases` covering contradiction/gaps, explicit trigger, email ambiguity, assumption warning, false positive, empty input, conflict, phase boundary, and score boundary.

risk:
- Legacy eval format prevents DoD validation and weakens activation coverage.

## SpokeReport - Script Engineer

status: pass

findings:
- A JSON report can deterministically encode findings, evidence tags, completeness, assumption ratio, evidence summary, and validation flags.

coverage_gaps:
- None after adding valid and negative fixtures.

recommended_changes:
- Run `bash skills/input-analysis/scripts/check.sh` before PR.

risk:
- Residual risk is limited to markdown-only outputs not converted into the JSON report contract.

## HardeningBrief

skill: `input-analysis`

scope_allowed:
- `skills/input-analysis/**`
- `docs/audits/skills/input-analysis-review.md`
- `docs/audits/skill-review-ledger.csv` row for `input-analysis`

required_changes:
- Deterministic assets and `assets/manifest.json`.
- Domain-specific examples and evals in DoD format.
- Offline report validator and fixtures.
- Review doc and ledger evidence after validation.

forbidden_changes:
- Other skills.
- Shared validators.
- Repo workflow or CI files.
- Unrelated ledger rows.

validation_plan:
- `bash skills/input-analysis/scripts/check.sh`
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill input-analysis`
- `python3 -B scripts/validate-skill-dod.py --skill input-analysis`
- Repo validation suite before PR.

merge_criteria:
- Per-skill validation passes.
- Repo validation passes.
- PR Quality Gates pass.
- Squash merge completes and branch cleanup succeeds.

## Evidence

Per-skill validation:
- `bash skills/input-analysis/scripts/check.sh`: passed; 2 valid fixtures accepted and 5 invalid fixtures rejected.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill input-analysis`: passed with `skills_with_scripts=1 warnings=0 errors=0`.
- `python3 -B scripts/validate-skill-dod.py --skill input-analysis`: passed with `dod=pass errors=0`.

Repo validation:
- `python3 -B scripts/validate-skills.py --strict`: passed with `skills=600 warnings=0 errors=0`.
- `python3 -B scripts/count-components.py --check-docs`: passed with `skills=600 agents=261 commands=267 prompts=256 components=1384`.
- `bash scripts/check-repo-boundaries.sh`: passed with `Repo boundaries OK`.
- `python3 -B scripts/qa/run-adversarial-tests.py`: passed with `summary: passed=11 failed=0 total=11`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks`: passed with `skills_with_scripts=71 warnings=0 errors=0`.
- `bash scripts/doc-factory/check.sh`: passed with deterministic smoke check.
- `git diff --check`: passed.

## Guardian Decision

Pass. Per-skill and repo validation are green, scope is confined to the active skill, the review doc exists, and the ledger row may be marked `dod-complete`.
