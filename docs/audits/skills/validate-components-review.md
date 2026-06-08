# Validate Components Review

## SpokeReport - Determinism Auditor

- status: pass
- findings: Base skill described component validation but lacked deterministic assets, report schema, and offline fixtures for pass/fail claims.
- coverage_gaps: Reports could claim docs alignment or clean component inventory without counts, validation evidence, or private path checks.
- recommended_changes: Add component report contract, count consistency policy, private component policy, and script-backed fixtures.
- risk: Future component types must be added to the count policy and report contract together.

## SpokeReport - Eval Designer

- status: pass
- findings: Evals now cover valid counts, missing counts, docs drift, private component inventory, failed findings claimed pass, clean claims without evidence, frontmatter field catalog checks, and count-command evidence.
- coverage_gaps: None remaining for this DoD scope.
- recommended_changes: Preserve both docs drift and private path cases in future eval edits.
- risk: Generated docs count expectations may change when new component classes are introduced.

## SpokeReport - Script Engineer

- status: pass
- findings: Added `scripts/validate_components_report.py`, `scripts/check.sh`, one valid fixture, and three invalid mutation fixtures.
- coverage_gaps: The validator checks structured audit reports; it does not run every component parser itself.
- recommended_changes: Use `scripts/count-components.py --check-docs` evidence for real repository counts.
- risk: Private path exclusions must remain fail-closed for publishable inventories.

## HardeningBrief

- skill: validate-components
- scope_allowed: `skills/validate-components/**`, `docs/audits/skills/validate-components-review.md`, and the `validate-components` ledger row.
- required_changes: Assets, manifest, eval cases, examples, offline validator, fixtures, review doc, ledger update, and generated index refresh if applicable.
- forbidden_changes: `validate-structure`, unrelated repo validators, unrelated skills, or unrelated ledger rows.
- validation_plan: Skill DoD, skill script contract, local check script, repo strict validation, docs count, repo boundaries, adversarial tests, doc-factory check, global script checks, adapter freshness, index freshness, and diff whitespace check.
- merge_criteria: Local validation green, PR ready, Quality Gates green, squash merge, branch cleanup, and updated `main`.

## Local Evidence

- `python3 -B scripts/validate-skill-dod.py --skill validate-components`: `skill=validate-components dod=pass errors=0`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill validate-components`: `skills_with_scripts=1 warnings=0 errors=0`.
- `bash skills/validate-components/scripts/check.sh`: `validate-components check passed: valid=1 invalid=3`.
- `python3 -B scripts/validate-skills.py --strict`: `skills=601 warnings=0 errors=0`.
- `python3 -B scripts/count-components.py --check-docs`: `skills=601 agents=261 commands=267 prompts=256 components=1385`.
- `bash scripts/check-repo-boundaries.sh`: `Repo boundaries OK`.
- `python3 -B scripts/qa/run-adversarial-tests.py`: `summary: passed=11 failed=0 total=11`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks`: `skills_with_scripts=139 warnings=0 errors=0`.
- `bash scripts/doc-factory/check.sh`: `OK: doc-factory deterministic smoke check passed`.
- `git diff --check origin/main...HEAD`: pass with no output.
- `git diff --check`: pass with no output.

## Guardian Decision

- status: pass
- decision: Authorize PR creation because the skill now has deterministic assets, evals, offline scripts, fixtures, review doc, reconciled ledger row, generated indexes, and passing local validation evidence.
- remaining_risks: The source branch contains `validate-structure`, but this isolated worktree must keep the diff scoped to `validate-components`.
