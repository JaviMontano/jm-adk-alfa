# Provenance Engineering Review

## SpokeReport - Determinism Auditor

- status: pass
- findings: Initial DoD failed because `assets/` was missing and evals did not require deterministic scripts or assets. The skill prose was specific, but no offline oracle validated claim-source invariants, source id inventory, conflict preservation, human escalation, render visibility, or structural tests.
- coverage_gaps: Empty `source_ids`, unknown source ids, averaged conflicts, missing escalation, hidden dates, and Guardian pass on invalid reports were not machine-checkable.
- recommended_changes: Add deterministic assets, evals, offline scripts, fixtures, review doc, and ledger reconciliation after validation.
- risk: Without structural checks, a pipeline can claim provenance while silently losing source ids or resolving conflicts.

## SpokeReport - Eval Designer

- status: pass
- findings: Updated evals to include deterministic assets and script checks across KYC, conflicting revenue, due diligence structural tests, explicit trigger, minimal input, false positives, anti-pattern requests, and unknown source ids.
- coverage_gaps: None remaining for this DoD hardening scope.
- recommended_changes: Keep evals tied to `assets`, `deterministic_scripts`, `typed_claim_source`, `conflict_marking`, `escalation_not_resolution`, `as_of_visible`, and `structural_test`.
- risk: Future eval edits could allow prose-only provenance without machine-verifiable source inventory.

## SpokeReport - Script Engineer

- status: pass
- findings: Added `scripts/validate_provenance_engineering.py`, `scripts/check.sh`, 2 valid fixtures, and 10 invalid mutation fixtures.
- coverage_gaps: The script validates JSON reports; implementation-language types still need local unit tests in the target pipeline.
- recommended_changes: Use the JSON report contract as a fixture oracle when porting the invariant into Python, TypeScript, or pipeline schemas.
- risk: Derived claims, joins, and normalization may need additional domain tests beyond this generic provenance contract.

## HardeningBrief

- skill: provenance-engineering
- scope_allowed: `skills/provenance-engineering/**`, `docs/audits/skills/provenance-engineering-review.md`, and the `provenance-engineering` ledger row.
- required_changes: Assets, eval cases, README/SKILL updates, offline scripts, fixtures, review doc, and ledger update after validation.
- forbidden_changes: Other skills, repo-level validators, unrelated docs, or unrelated ledger rows.
- validation_plan: Skill DoD, skill script contract, local check script, repo strict validation, docs count, repo boundaries, adversarial tests, doc-factory check, global script checks, and diff whitespace check.
- merge_criteria: Local validation green, PR ready, Quality Gates green, squash merge, branch cleanup, and updated `main`.

## Local Evidence

- `bash skills/provenance-engineering/scripts/check.sh`: `provenance-engineering check passed: valid=2 invalid=10`.
- `python3 -B scripts/validate-skill-dod.py --skill provenance-engineering`: `skill=provenance-engineering dod=pass errors=0`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill provenance-engineering`: `skills_with_scripts=1 warnings=0 errors=0`.
- `python3 -B scripts/validate-skills.py --strict`: `skills=600 warnings=0 errors=0`.
- `python3 -B scripts/count-components.py --check-docs`: `skills=600 agents=261 commands=267 prompts=256 components=1384`.
- `bash scripts/check-repo-boundaries.sh`: `Repo boundaries OK`.
- `python3 -B scripts/qa/run-adversarial-tests.py`: `summary: passed=11 failed=0 total=11`.
- `bash scripts/doc-factory/check.sh`: `OK: doc-factory deterministic smoke check passed`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks`: `skills_with_scripts=115 warnings=0 errors=0`.
- `git diff --check`: pass with no output.

## Guardian Decision

- status: pass
- decision: Authorize PR creation because the skill now has deterministic assets, evals, offline scripts, fixtures, review doc, reconciled ledger row, and passing local validation evidence.
- remaining_risks: Target pipelines still need language-specific tests to enforce the same invariant at construction time.
