# prompt-chaining-design Review

## SpokeReport - Determinism Auditor

- status: pass
- findings: Initial DoD failed because `assets/` was missing and evals did not require deterministic scripts. Existing skill prose described the chaining pattern, but no offline oracle validated chain justification, local pass isolation, transition schema, summaries-only integration, or typed error propagation.
- coverage_gaps: Integration over raw units, missing transition schema, global exception failures, local pass over multiple units, unjustified chaining, and Guardian pass on blocked cases were not machine-checkable.
- recommended_changes: Add deterministic assets, evals, offline scripts, fixtures, review doc, and ledger reconciliation.
- risk: Without these checks, the skill could recommend prompt chaining while silently falling back to a mega-prompt or untyped glue.

## SpokeReport - Eval Designer

- status: pass
- findings: Replaced generic eval checks with 10 deterministic scenarios covering repo audit, explicit trigger, transition schema, parallel map/reduce, unrelated false positive, empty input, single-pass fit, raw integration rejection, global exception rejection, and upgrade safety.
- coverage_gaps: None remaining for this DoD hardening scope.
- recommended_changes: Keep evals tied to `assets`, `deterministic_scripts`, `chain_justification`, `local_pass_schema`, `transition_schema`, `integration_summaries_only`, and `typed_error_state`.
- risk: Future eval edits could weaken the no-raw-data boundary between local and integration passes.

## SpokeReport - Script Engineer

- status: pass
- findings: Added `scripts/validate_prompt_chaining_design.py`, `scripts/check.sh`, 2 valid fixtures, and 10 invalid mutation fixtures.
- coverage_gaps: The script validates structured JSON reports; prose-only chain descriptions still require Guardian review against the same contract.
- recommended_changes: Use the JSON contract whenever prompt chaining architecture must be reproducible offline.
- risk: Free-form prose can hide raw-data shortcuts unless reviewed against the contract.

## HardeningBrief

- skill: prompt-chaining-design
- scope_allowed: `skills/prompt-chaining-design/**`, `docs/audits/skills/prompt-chaining-design-review.md`, and the `prompt-chaining-design` ledger row.
- required_changes: Assets, eval cases, README/SKILL updates, offline scripts, fixtures, review doc, and ledger update after validation.
- forbidden_changes: Other skills, repo-level validators, unrelated docs, or unrelated ledger rows.
- validation_plan: Skill DoD, skill script contract, local check script, repo strict validation, docs count, repo boundaries, adversarial tests, doc-factory check, adapter freshness, global script checks, and diff whitespace check.
- merge_criteria: Local validation green, PR ready, Quality Gates green, squash merge, branch cleanup, and updated `main`.

## Local Evidence

- `bash skills/prompt-chaining-design/scripts/check.sh`: `prompt-chaining-design check passed: valid=2 invalid=10`.
- `python3 -B scripts/validate-skill-dod.py --skill prompt-chaining-design`: `skill=prompt-chaining-design dod=pass errors=0`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill prompt-chaining-design`: `skills_with_scripts=1 warnings=0 errors=0`.
- `python3 -B scripts/validate-skills.py --strict`: `skills=600 warnings=0 errors=0`.
- `python3 -B scripts/count-components.py --check-docs`: `skills=600 agents=261 commands=267 prompts=256 components=1384`.
- `bash scripts/check-repo-boundaries.sh`: `Repo boundaries OK`.
- `python3 -B scripts/qa/run-adversarial-tests.py`: `summary: passed=11 failed=0 total=11`.
- `bash scripts/doc-factory/check.sh`: `OK: doc-factory deterministic smoke check passed`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks`: `skills_with_scripts=112 warnings=0 errors=0`.
- `bash scripts/adapt.sh all`: `ADAPTER-COMPLETE` for antigravity, vscode, cursor+windsurf, and agents+gemini with no core files modified.
- `git diff --check`: pass with no output.

## Guardian Decision

- status: pass
- decision: Authorize PR creation because the skill now has deterministic assets, evals, offline scripts, fixtures, review doc, adapter freshness evidence, a reconciled ledger row, and passing local validation.
- remaining_risks: Prose-only prompt-chain designs require human review against the JSON contract before they can be treated as deterministic evidence.
