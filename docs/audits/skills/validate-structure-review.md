# Validate Structure Review

## SpokeReport - Determinism Auditor

- status: pass
- findings: Base skill described layout validation but lacked deterministic assets, report schema, and offline fixtures for clean structure claims.
- coverage_gaps: Reports could claim a clean plugin structure without validation evidence or while private/transient paths were publishable.
- recommended_changes: Add structure report contract, private/transient policy, clean-claim policy, and script-backed fixtures.
- risk: New plugin layout conventions must be added to the contract and evals together.

## SpokeReport - Eval Designer

- status: pass
- findings: Evals now cover clean structure, clean claim without evidence, unresolved critical findings, private publishable paths, transient publishable paths, component layout failures, path traversal, and script permission evidence.
- coverage_gaps: None remaining for this DoD scope.
- recommended_changes: Preserve sensitive-path and path-traversal cases in future eval edits.
- risk: Official plugin spec changes may require updating severity expectations.

## SpokeReport - Script Engineer

- status: pass
- findings: Added `scripts/validate_structure_report.py`, `scripts/check.sh`, one valid fixture, and three invalid mutation fixtures.
- coverage_gaps: The validator checks structured reports; it does not walk arbitrary plugin trees directly.
- recommended_changes: Use real structure scan evidence before claiming clean structure in production reports.
- risk: Private and transient path handling must remain fail-closed for publishable inventories.

## HardeningBrief

- skill: validate-structure
- scope_allowed: `skills/validate-structure/**`, `docs/audits/skills/validate-structure-review.md`, and the `validate-structure` ledger row.
- required_changes: Assets, manifest, eval cases, examples, offline validator, fixtures, review doc, ledger update, and generated index refresh if applicable.
- forbidden_changes: unrelated repo validators, unrelated skills, or unrelated ledger rows.
- validation_plan: Skill DoD, skill script contract, local check script, repo strict validation, docs count, repo boundaries, adversarial tests, doc-factory check, global script checks, adapter freshness, index freshness, and diff whitespace check.
- merge_criteria: Local validation green, PR ready, Quality Gates green, squash merge, branch cleanup, and updated `main`.

## Local Evidence

- `python3 -B scripts/validate-skill-dod.py --skill validate-structure`: `skill=validate-structure dod=pass errors=0`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill validate-structure`: `skills_with_scripts=1 warnings=0 errors=0`.
- `bash skills/validate-structure/scripts/check.sh`: `validate-structure check passed: valid=1 invalid=3`.
- `python3 -B scripts/validate-skills.py --strict`: `skills=601 warnings=0 errors=0`.
- `python3 -B scripts/count-components.py --check-docs`: `skills=601 agents=261 commands=267 prompts=256 components=1385`.
- `bash scripts/check-repo-boundaries.sh`: `Repo boundaries OK`.
- `python3 -B scripts/qa/run-adversarial-tests.py`: `summary: passed=11 failed=0 total=11`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks`: `skills_with_scripts=140 warnings=0 errors=0`.
- `bash scripts/doc-factory/check.sh`: `OK: doc-factory deterministic smoke check passed`.
- `git diff --check origin/main...HEAD`: pass with no output.
- `git diff --check`: pass with no output.

## Guardian Decision

- status: pass
- decision: Authorize PR creation because the skill now has deterministic assets, evals, offline scripts, fixtures, review doc, reconciled ledger row, generated indexes, and passing local validation evidence.
- remaining_risks: None identified within isolated `validate-structure` scope.
