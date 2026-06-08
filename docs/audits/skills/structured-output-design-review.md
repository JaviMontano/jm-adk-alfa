# Structured Output Design Review

## SpokeReport - Determinism Auditor

- status: pass
- findings: Initial DoD failed because `assets/` was missing and eval cases did not require deterministic scripts or assets.
- coverage_gaps: JSON Schema closure, nullable unions, enum escape fields, forced tool choice, typed parse source, and failure routing were not machine-checkable.
- recommended_changes: Add deterministic assets, offline validator, valid and invalid fixtures, specialized evals, review doc, and ledger reconciliation after validation.
- risk: Without a validator, the skill can drift back to prose JSON plus `json.loads(text)`.

## SpokeReport - Eval Designer

- status: pass
- findings: Evals now cover happy path, explicit trigger, minimal input, rich context, nullable cleanup, enum escape, forced tool choice, false positives, empty input, conflicting text-only request, free-text fallback degradation, multi-tool boundary, and upgrade safety.
- coverage_gaps: None remaining for this DoD hardening scope.
- recommended_changes: Keep evals tied to `assets`, `deterministic_scripts`, `schema_closed`, `nullable_union_used`, `enum_escape_present`, `tool_choice_forced`, and `typed_parse_source`.
- risk: Future eval edits could permit loose schemas or free-text fallback.

## SpokeReport - Script Engineer

- status: pass
- findings: Added `scripts/validate_structured_output_design.py`, `scripts/check.sh`, 2 valid fixtures, and 12 invalid mutation fixtures.
- coverage_gaps: The script validates design packages; it does not call an LLM or a live API.
- recommended_changes: Use the JSON contract whenever a structured output design is consumed by code.
- risk: Provider-specific JSON Schema dialect changes may require future policy updates.

## HardeningBrief

- skill: structured-output-design
- scope_allowed: `skills/structured-output-design/**`, `docs/audits/skills/structured-output-design-review.md`, and the `structured-output-design` ledger row.
- required_changes: Assets, eval cases, README/SKILL updates, offline scripts, fixtures, review doc, and ledger update after validation.
- forbidden_changes: Other skills, repo-level validators, unrelated docs, or unrelated ledger rows.
- validation_plan: Skill DoD, skill script contract, local check script, repo strict validation, docs count, repo boundaries, adversarial tests, doc-factory check, global script checks, and diff whitespace check.
- merge_criteria: Local validation green, PR ready, Quality Gates green, squash merge, branch cleanup, and updated `main`.

## Local Evidence

- `bash skills/structured-output-design/scripts/check.sh`: `structured-output-design check passed: valid=2 invalid=12`.
- `python3 -B scripts/validate-skill-dod.py --skill structured-output-design`: `skill=structured-output-design dod=pass errors=0`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill structured-output-design`: `skills_with_scripts=1 warnings=0 errors=0`.
- `python3 -B scripts/validate-skills.py --strict`: `skills=600 warnings=0 errors=0`.
- `python3 -B scripts/count-components.py --check-docs`: `skills=600 agents=261 commands=267 prompts=256 components=1384`.
- `bash scripts/check-repo-boundaries.sh`: `Repo boundaries OK`.
- `python3 -B scripts/qa/run-adversarial-tests.py`: `summary: passed=11 failed=0 total=11`.
- `bash scripts/doc-factory/check.sh`: `OK: doc-factory deterministic smoke check passed`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks`: `skills_with_scripts=119 warnings=0 errors=0`.
- `git diff --check`: pass with no output.

## Guardian Decision

- status: pass
- decision: Authorize PR creation because the skill now has deterministic assets, evals, offline scripts, fixtures, review doc, reconciled ledger row, and passing local validation evidence.
- remaining_risks: Provider-specific schema dialect changes may require future updates to assets.
