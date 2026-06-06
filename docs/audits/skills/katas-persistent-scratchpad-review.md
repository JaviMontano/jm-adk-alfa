# katas-persistent-scratchpad Review

Date: 2026-06-06
Branch: `codex/harden-katas-persistent-scratchpad-dod-20260606`
Status: dod-complete; local validation passed

## Scope

- Allowed: `skills/katas-persistent-scratchpad/**`
- Allowed: `docs/audits/skills/katas-persistent-scratchpad-review.md`
- Allowed after full local validation: the `katas-persistent-scratchpad` row in `docs/audits/skill-review-ledger.csv`
- Forbidden: other skills, shared validators, CI, unrelated docs, or cross-skill edits

## SpokeReport - Determinism Auditor

status: warn

findings:
- The skill is domain-specific and already explains persistent disk scratchpads, fixed sections, validated conclusions, read-once access, compact survival, and anti-patterns.
- DoD failed before hardening because `assets/` was missing and eval expected checks did not include `assets` or `deterministic_scripts`.

coverage_gaps:
- No assetized contract for path, sections, evidence, read-once access, append-only writes, exclusions, or report shape.
- No offline validator for missing evidence, re-read-per-turn behavior, internal monologue, overwrites, missing sections, or conversation-only memory.

recommended_changes:
- Add deterministic assets and manifest.
- Add script fixtures and validator.
- Harden eval expected checks.

risk:
- Without offline validation, a scratchpad could persist unvalidated noise, overwrite curated entries, or depend on volatile conversation state.

## SpokeReport - Eval Designer

status: warn

findings:
- Existing evals include realistic domain cases, but expected checks were generic.
- Boundary cases did not enforce assets/scripts or append/no-overwrite behavior.

coverage_gaps:
- Missing explicit assets/scripts checks.
- Missing deterministic checks for missing evidence, internal monologue, unconfirmed hypotheses, re-reading, append-only updates, and degradation when evidence is missing.

recommended_changes:
- Add `assets`, `deterministic_scripts`, and domain-specific expected checks to eval cases.
- Back the cases with offline fixtures.

risk:
- Activation could be correct while the scratchpad contract remains unverifiable.

## SpokeReport - Script Engineer

status: pass

findings:
- A local JSON validator adds real deterministic coverage because the scratchpad report has fixed sections and boolean policies that can be checked offline.

coverage_gaps:
- None after adding valid and negative fixtures.

recommended_changes:
- Run `bash skills/katas-persistent-scratchpad/scripts/check.sh` before PR.

risk:
- Residual risk is limited to markdown-only outputs not converted into the JSON report contract.

## HardeningBrief

skill: `katas-persistent-scratchpad`

scope_allowed:
- `skills/katas-persistent-scratchpad/**`
- `docs/audits/skills/katas-persistent-scratchpad-review.md`
- `docs/audits/skill-review-ledger.csv` row for `katas-persistent-scratchpad`

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
- `bash skills/katas-persistent-scratchpad/scripts/check.sh`
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill katas-persistent-scratchpad`
- `python3 -B scripts/validate-skill-dod.py --skill katas-persistent-scratchpad`
- Repo validation suite before PR.

merge_criteria:
- Per-skill validation passes.
- Repo validation passes.
- PR Quality Gates pass.
- Squash merge completes and branch cleanup succeeds.

## Evidence

Per-skill validation:
- `bash skills/katas-persistent-scratchpad/scripts/check.sh`: passed; 2 valid fixtures accepted and 6 invalid fixtures rejected.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill katas-persistent-scratchpad`: passed with `skills_with_scripts=1 warnings=0 errors=0`.
- `python3 -B scripts/validate-skill-dod.py --skill katas-persistent-scratchpad`: passed with `dod=pass errors=0`.

Repo validation:
- `python3 -B scripts/validate-skills.py --strict`: passed with `skills=600 warnings=0 errors=0`.
- `python3 -B scripts/count-components.py --check-docs`: passed with `skills=600 agents=261 commands=267 prompts=256 components=1384`.
- `bash scripts/check-repo-boundaries.sh`: passed with `Repo boundaries OK`.
- `python3 -B scripts/qa/run-adversarial-tests.py`: passed with `summary: passed=11 failed=0 total=11`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks`: passed with `skills_with_scripts=69 warnings=0 errors=0`.
- `bash scripts/doc-factory/check.sh`: passed with deterministic smoke check.
- `git diff --check`: passed.

## Guardian Decision

Pass. Per-skill and repo validation are green, scope is confined to the active skill, the review doc exists, and the ledger row may be marked `dod-complete`.
