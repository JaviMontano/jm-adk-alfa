# pristino-calibration Review

## SpokeReport - Determinism Auditor

- status: pass
- findings: Initial DoD failed because `assets/` was missing, knowledge/examples/evals retained generic scaffold markers, evals did not require deterministic scripts, and no offline oracle existed for persona line, mode shape, precedence, evidence tags, Canvas or delegates.
- coverage_gaps: Bypass mode, solo modes, full substantive Canvas, low confidence handling, invented delegate agents, missing evidence tags, and Guardian pass on broken calibration were not machine-checkable.
- recommended_changes: Add deterministic assets, specialized evals, examples, knowledge, offline scripts, fixtures, review doc, and ledger reconciliation.
- risk: Without these checks, the runtime could claim calibration while omitting the actual persona/optimizer contract.

## SpokeReport - Eval Designer

- status: pass
- findings: Replaced generic eval checks with 10 deterministic cases covering full substantive Canvas, bypass, solo prompt, solo response, low confidence, precedence conflict, invented delegate, degraded self-calibration, empty input, and upgrade safety.
- coverage_gaps: None remaining for this DoD hardening scope.
- recommended_changes: Keep evals tied to `assets`, `deterministic_scripts`, `persona_line`, `optimizer_sections`, `precedence_order`, `evidence_tags`, and `canvas_contract`.
- risk: Future eval edits could weaken guarantees around exact output shape per mode.

## SpokeReport - Script Engineer

- status: pass
- findings: Added `scripts/validate_pristino_calibration.py`, `scripts/check.sh`, 2 valid fixtures, and 10 invalid mutation fixtures.
- coverage_gaps: The script validates structured JSON calibration reports; prose-only responses still require Guardian review against the same contract.
- recommended_changes: Use the JSON contract whenever persona calibration compliance must be reproducible offline.
- risk: Free-form responses can drift unless reviewed against the field-level contract.

## HardeningBrief

- skill: pristino-calibration
- scope_allowed: `skills/pristino-calibration/**`, `docs/audits/skills/pristino-calibration-review.md`, and the `pristino-calibration` ledger row.
- required_changes: Assets, examples, eval cases, knowledge, offline scripts, fixtures, review doc, and ledger update after validation.
- forbidden_changes: Other skills, repo-level validators, unrelated docs, or unrelated ledger rows.
- validation_plan: Skill DoD, skill script contract, local check script, repo strict validation, docs count, repo boundaries, adversarial tests, doc-factory check, adapter freshness, global script checks, and diff whitespace check.
- merge_criteria: Local validation green, PR ready, Quality Gates green, squash merge, branch cleanup, and updated `main`.

## Local Evidence

- `bash skills/pristino-calibration/scripts/check.sh`: `pristino-calibration check passed: valid=2 invalid=10`.
- `python3 -B scripts/validate-skill-dod.py --skill pristino-calibration`: `skill=pristino-calibration dod=pass errors=0`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill pristino-calibration`: `skills_with_scripts=1 warnings=0 errors=0`.
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
- remaining_risks: Prose-only calibration outputs require human review against the JSON contract before they can be treated as deterministic evidence.
