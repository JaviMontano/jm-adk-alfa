# Repository Organization Review

## SpokeReport - Determinism Auditor

- status: pass
- findings: Base skill had generic activation evals and no deterministic assets, manifest, or offline validator for repository organization claims.
- coverage_gaps: Cleanup and organization reports could claim a clean repository without scan evidence, move manifests, or private path boundary checks.
- recommended_changes: Add explicit contracts for organization reports, transient placement, move manifests, and private boundary handling.
- risk: Future organization policies may need extra path classes for generated worktrees or temporary CI artifacts.

## SpokeReport - Eval Designer

- status: pass
- findings: Evals now include eight deterministic cases covering valid reports, private publish blocking, missing manifests, clean-claim false positives, transient placement, private inventory-only handling, rename manifest requirements, and evidence requirements.
- coverage_gaps: None remaining for this DoD scope.
- recommended_changes: Keep false-positive and degradation cases when editing evals.
- risk: Larger repository scans may need fixture snapshots if scan output itself becomes part of validation.

## SpokeReport - Script Engineer

- status: pass
- findings: Added `scripts/validate_repository_organization_report.py`, `scripts/check.sh`, one valid fixture, and three invalid mutation fixtures.
- coverage_gaps: The validator checks structured reports; it does not execute filesystem moves.
- recommended_changes: Keep destructive actions represented as manifest-only report entries.
- risk: SHA and manifest requirements should remain fail-closed for move, archive, delete, and rename actions.

## HardeningBrief

- skill: repository-organization
- scope_allowed: `skills/repository-organization/**`, `docs/audits/skills/repository-organization-review.md`, and the `repository-organization` ledger row.
- required_changes: Assets, manifest, eval cases, examples, offline validator, fixtures, review doc, ledger update, and generated index refresh.
- forbidden_changes: `secrets-sanitization`, `validate-components`, `validate-structure`, unrelated skills, repo validators, or unrelated ledger rows.
- validation_plan: Skill DoD, skill script contract, local check script, repo strict validation, docs count, repo boundaries, adversarial tests, doc-factory check, global script checks where local process budget allows, adapter freshness, index freshness, and diff whitespace check.
- merge_criteria: Local validation green, PR ready, Quality Gates green, squash merge, branch cleanup, and updated `main`.

## Local Evidence

- `python3 -B scripts/validate-skill-dod.py --skill repository-organization`: `skill=repository-organization dod=pass errors=0`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill repository-organization`: `skills_with_scripts=1 warnings=0 errors=0`.
- `bash skills/repository-organization/scripts/check.sh`: `repository-organization check passed: valid=1 invalid=3`.
- `python3 -B scripts/validate-skills.py --strict`: `skills=601 warnings=0 errors=0`.
- `python3 -B scripts/count-components.py --check-docs`: `skills=601 agents=261 commands=267 prompts=256 components=1385`.
- `bash scripts/check-repo-boundaries.sh`: `Repo boundaries OK`.
- `python3 -B scripts/qa/run-adversarial-tests.py`: `summary: passed=11 failed=0 total=11`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks`: `skills_with_scripts=137 warnings=0 errors=0`.
- `bash scripts/doc-factory/check.sh`: `OK: doc-factory deterministic smoke check passed`.
- `git diff --check origin/main...HEAD`: pass with no output.
- `git diff --check`: pass with no output.

## Guardian Decision

- status: pass
- decision: Authorize PR creation because the skill now has deterministic assets, evals, offline scripts, fixtures, review doc, reconciled ledger row, generated indexes, and passing local validation evidence.
- remaining_risks: The source branch contains other repo-structure skills, but this isolated worktree must keep the diff scoped to `repository-organization`.
