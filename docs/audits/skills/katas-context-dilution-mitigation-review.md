# katas-context-dilution-mitigation Review

Date: 2026-06-06
Branch: `codex/harden-katas-context-dilution-mitigation-dod-20260606`
Status: dod-complete; local validation passed

## Scope

- Allowed: `skills/katas-context-dilution-mitigation/**`
- Allowed: `docs/audits/skills/katas-context-dilution-mitigation-review.md`
- Allowed after full local validation: the `katas-context-dilution-mitigation` row in `docs/audits/skill-review-ledger.csv`
- Forbidden: other skills, shared validators, CI, unrelated docs, or cross-skill edits

## SpokeReport - Determinism Auditor

status: warn

findings:
- The skill is domain-specific and already explains the U-shaped attention curve, edge placement, 0.55 compaction, and preservation of rules, decisions, and escalations.
- DoD failed before hardening because `assets/` was missing and eval expected checks did not include `assets` or `deterministic_scripts`.

coverage_gaps:
- No deterministic asset contract for attention curve, edge placement, threshold, preserve list, or report shape.
- No offline validator to reject middle-only critical rules, late thresholds, dropping rules, missing compaction above threshold, or bulk context at edges.

recommended_changes:
- Add deterministic assets and manifest.
- Add offline script fixtures and validator.
- Harden eval expected checks.

risk:
- Without offline validation, a prompt could bury critical rules or compact away policy state while still claiming mitigation.

## SpokeReport - Eval Designer

status: warn

findings:
- Existing evals are mostly domain-specific, but expected checks were generic and missed assets/scripts.
- Weak upgrade/local cases did not test threshold or preservation boundaries.

coverage_gaps:
- Missing explicit edge placement, compaction threshold, preserve-rules, and rejection checks.

recommended_changes:
- Add `assets`, `deterministic_scripts`, edge placement, threshold, and preservation checks to evals.
- Back the cases with offline fixtures.

risk:
- The kata could activate correctly but fail to prove that critical rules remain in high-attention positions.

## SpokeReport - Script Engineer

status: pass

findings:
- A JSON report can deterministically encode critical rules, placement, usage fraction, threshold, compaction policy, and validation flags.

coverage_gaps:
- None after adding valid and negative fixtures.

recommended_changes:
- Run `bash skills/katas-context-dilution-mitigation/scripts/check.sh` before PR.

risk:
- Residual risk is limited to markdown-only outputs not converted into the JSON report contract.

## HardeningBrief

skill: `katas-context-dilution-mitigation`

scope_allowed:
- `skills/katas-context-dilution-mitigation/**`
- `docs/audits/skills/katas-context-dilution-mitigation-review.md`
- `docs/audits/skill-review-ledger.csv` row for `katas-context-dilution-mitigation`

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
- `bash skills/katas-context-dilution-mitigation/scripts/check.sh`
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill katas-context-dilution-mitigation`
- `python3 -B scripts/validate-skill-dod.py --skill katas-context-dilution-mitigation`
- Repo validation suite before PR.

merge_criteria:
- Per-skill validation passes.
- Repo validation passes.
- PR Quality Gates pass.
- Squash merge completes and branch cleanup succeeds.

## Evidence

Per-skill validation:
- `bash skills/katas-context-dilution-mitigation/scripts/check.sh`: passed; 2 valid fixtures accepted and 5 invalid fixtures rejected.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill katas-context-dilution-mitigation`: passed with `skills_with_scripts=1 warnings=0 errors=0`.
- `python3 -B scripts/validate-skill-dod.py --skill katas-context-dilution-mitigation`: passed with `dod=pass errors=0`.

Repo validation:
- `python3 -B scripts/validate-skills.py --strict`: passed with `skills=600 warnings=0 errors=0`.
- `python3 -B scripts/count-components.py --check-docs`: passed with `skills=600 agents=261 commands=267 prompts=256 components=1384`.
- `bash scripts/check-repo-boundaries.sh`: passed with `Repo boundaries OK`.
- `python3 -B scripts/qa/run-adversarial-tests.py`: passed with `summary: passed=11 failed=0 total=11`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks`: passed with `skills_with_scripts=70 warnings=0 errors=0`.
- `bash scripts/doc-factory/check.sh`: passed with deterministic smoke check.
- `git diff --check`: passed.

## Guardian Decision

Pass. Per-skill and repo validation are green, scope is confined to the active skill, the review doc exists, and the ledger row may be marked `dod-complete`.
