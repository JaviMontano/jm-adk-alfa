# Prompting And Meta Prompting Review

## SpokeReport - Determinism Auditor

- status: pass
- findings: Initial DoD failed because `assets/` was missing, examples and knowledge still contained scaffold text, and evals did not require deterministic scripts or assets.
- coverage_gaps: Prompt contract completeness, meta-prompt review dimensions, verifiable acceptance criteria, edge eval coverage, safety boundaries, and Guardian consistency were not machine-checkable.
- recommended_changes: Add deterministic assets, specialized evals, offline validator, fixtures, examples, review doc, and ledger reconciliation after validation.
- risk: Without a structural contract, a prompt can look polished while missing output shape, evidence policy, safety gates, or eval coverage.

## SpokeReport - Eval Designer

- status: pass
- findings: Replaced generic evals with 10 deterministic scenarios covering happy path, explicit trigger, minimal input, rich meta-prompt context, false positive, empty input, conflicting requirements, secret capture, hidden chain-of-thought, upgrade safety, and eval coverage.
- coverage_gaps: None remaining for this DoD hardening scope.
- recommended_changes: Keep evals tied to `assets`, `deterministic_scripts`, `prompt_contract`, `meta_prompt`, `acceptance_criteria`, `eval_cases`, and `safety_boundaries`.
- risk: Future eval edits could overfit to happy-path prompt writing and miss unsafe prompt optimization.

## SpokeReport - Script Engineer

- status: pass
- findings: Added `scripts/validate_prompting_and_meta_prompting.py`, `scripts/check.sh`, 2 valid fixtures, and 10 invalid mutation fixtures.
- coverage_gaps: The script validates JSON prompt-system reports; prose-only prompt artifacts still require Guardian review against the same contract.
- recommended_changes: Use the JSON contract whenever reusable prompts or meta-prompts must be treated as deterministic evidence.
- risk: Free-form prompts can hide missing-data or safety gaps unless converted to the report shape.

## HardeningBrief

- skill: prompting-and-meta-prompting
- scope_allowed: `skills/prompting-and-meta-prompting/**`, `docs/audits/skills/prompting-and-meta-prompting-review.md`, and the `prompting-and-meta-prompting` ledger row.
- required_changes: Assets, eval cases, README/SKILL updates, offline scripts, fixtures, review doc, and ledger update after validation.
- forbidden_changes: Other skills, repo-level validators, unrelated docs, or unrelated ledger rows.
- validation_plan: Skill DoD, skill script contract, local check script, repo strict validation, docs count, repo boundaries, adversarial tests, doc-factory check, global script checks, and diff whitespace check.
- merge_criteria: Local validation green, PR ready, Quality Gates green, squash merge, branch cleanup, and updated `main`.

## Local Evidence

- `bash skills/prompting-and-meta-prompting/scripts/check.sh`: `prompting-and-meta-prompting check passed: valid=2 invalid=10`.
- `python3 -B scripts/validate-skill-dod.py --skill prompting-and-meta-prompting`: `skill=prompting-and-meta-prompting dod=pass errors=0`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill prompting-and-meta-prompting`: `skills_with_scripts=1 warnings=0 errors=0`.
- `python3 -B scripts/validate-skills.py --strict`: `skills=600 warnings=0 errors=0`.
- `python3 -B scripts/count-components.py --check-docs`: `skills=600 agents=261 commands=267 prompts=256 components=1384`.
- `bash scripts/check-repo-boundaries.sh`: `Repo boundaries OK`.
- `python3 -B scripts/qa/run-adversarial-tests.py`: `summary: passed=11 failed=0 total=11`.
- `bash scripts/doc-factory/check.sh`: `OK: doc-factory deterministic smoke check passed`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks`: `skills_with_scripts=114 warnings=0 errors=0`.
- `git diff --check`: pass with no output.

## Guardian Decision

- status: pass
- decision: Authorize PR creation because the skill now has deterministic assets, evals, offline scripts, fixtures, review doc, reconciled ledger row, and passing local validation evidence.
- remaining_risks: Prose-only prompt designs require human review against the JSON contract before they can be treated as deterministic evidence.
