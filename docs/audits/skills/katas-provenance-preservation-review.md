# katas-provenance-preservation Review

## SpokeReport - Determinism Auditor

- status: pass
- findings: Initial DoD failed because `assets/` was missing and evals did not include `assets` or `deterministic_scripts`. Multiple files retained scaffold headers.
- coverage_gaps: No offline oracle existed for orphan claims, unknown source refs, missing publication dates, silenced conflicts, forbidden conflict resolution, free-prose-only summaries, or structural test failure.
- recommended_changes: Add deterministic assets, eval cases, specialized examples, prompts, agents, templates, knowledge, offline scripts, fixtures, review doc, and ledger update.
- risk: Without these changes, factual reports could look correct while losing claim-level auditability.

## SpokeReport - Eval Designer

- status: pass
- findings: Replaced eval data with 10 deterministic cases covering company report provenance, conflict escalation, orphan claims, unknown source refs, newest-wins rejection, subagent aggregation, free-prose rejection, false positives, and upgrade safety.
- coverage_gaps: None remaining for the DoD hardening scope.
- recommended_changes: Keep evals tied to `assets`, `deterministic_scripts`, and `quality_criteria`.
- risk: Future edits could weaken guarantees if orphan-claim or conflict-preservation cases are removed.

## SpokeReport - Script Engineer

- status: pass
- findings: Added `scripts/validate_provenance_preservation.py`, `scripts/check.sh`, 2 valid fixtures, and 8 invalid mutation fixtures.
- coverage_gaps: The script validates structured JSON provenance reports, not arbitrary free-form Markdown.
- recommended_changes: Use the JSON contract whenever a provenance-preserving report must be checked offline.
- risk: Markdown-only deliverables still require Guardian review against the same deterministic contract.

## HardeningBrief

- skill: katas-provenance-preservation
- scope_allowed: `skills/katas-provenance-preservation/**`, `docs/audits/skills/katas-provenance-preservation-review.md`, and the `katas-provenance-preservation` ledger row.
- required_changes: Assets, examples, eval cases, prompts, agents, templates, knowledge, offline scripts, fixtures, review doc, and ledger update.
- forbidden_changes: Other skills, adapters generated from canonical files, repo-level validators, unrelated docs, or unrelated ledger rows.
- validation_plan: Skill DoD, skill script contract, local check script, repo strict validation, docs count, repo boundaries, adversarial tests, doc-factory check, adapter freshness, global script checks, and diff whitespace check.
- merge_criteria: Local validation green, PR ready, Quality Gates green, squash merge, branch cleanup, and updated `main`.

## Local Evidence

- `bash skills/katas-provenance-preservation/scripts/check.sh`: `katas-provenance-preservation check passed: valid=2 invalid=8`.
- `python3 -B scripts/validate-skill-dod.py --skill katas-provenance-preservation`: `skill=katas-provenance-preservation dod=pass errors=0`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill katas-provenance-preservation`: `skills_with_scripts=1 warnings=0 errors=0`.
- `python3 -B scripts/validate-skills.py --strict`: `skills=600 warnings=0 errors=0`.
- `python3 -B scripts/count-components.py --check-docs`: `skills=600 agents=261 commands=267 prompts=256 components=1384`.
- `bash scripts/check-repo-boundaries.sh`: `Repo boundaries OK`.
- `python3 -B scripts/qa/run-adversarial-tests.py`: `summary: passed=11 failed=0 total=11`.
- `bash scripts/doc-factory/check.sh`: `OK: doc-factory deterministic smoke check passed`.
- `bash scripts/adapt.sh all` plus adapter diff check: `adapter freshness OK`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks`: `skills_with_scripts=105 warnings=0 errors=0`.
- `git diff --check`: pass with no output.

## Guardian Decision

- status: pass
- decision: Authorize PR creation because the ledger row is updated and all local checks passed.
- remaining_risks: Markdown-only provenance reports require human review against the same deterministic JSON contract.
