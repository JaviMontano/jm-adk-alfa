# Runtime Routing Review

## SpokeReport - Determinism Auditor

- status: pass
- findings: Initial DoD failed because `assets/` was missing, scaffold text remained in knowledge and examples, and evals did not require deterministic scripts or assets.
- coverage_gaps: Runtime evidence, capability matrix, lowest-permission selection, validation limits, fallback, and Guardian consistency were not machine-checkable.
- recommended_changes: Add deterministic assets, specialized evals, offline validator, fixtures, review doc, and ledger reconciliation after validation.
- risk: Without evidence-grounded routing, the skill can claim runtime support that has not been observed.

## SpokeReport - Eval Designer

- status: pass
- findings: Replaced generic evals with deterministic cases covering Codex local routing, explicit trigger, minimal input, MCP pending state, false positive, empty input, unsupported runtime claims, remote secret boundary, upgrade safety, and fallback requirements.
- coverage_gaps: None remaining for this DoD hardening scope.
- recommended_changes: Keep evals tied to `assets`, `deterministic_scripts`, `capability_matrix`, `evidence_grounding`, `lowest_permission`, `validation_limits`, and `fallback`.
- risk: Future eval edits could reintroduce unsupported runtime assertions.

## SpokeReport - Script Engineer

- status: pass
- findings: Added `scripts/validate_runtime_routing.py`, `scripts/check.sh`, 2 valid fixtures, and 10 invalid mutation fixtures.
- coverage_gaps: The script validates JSON routing reports; live runtime capabilities still require executed checks in the target environment.
- recommended_changes: Use the JSON contract whenever a route recommendation affects file access, tooling, or secret boundaries.
- risk: Adapter docs prove possible support, not active session support.

## HardeningBrief

- skill: runtime-routing
- scope_allowed: `skills/runtime-routing/**`, `docs/audits/skills/runtime-routing-review.md`, and the `runtime-routing` ledger row.
- required_changes: Assets, eval cases, README/SKILL updates, offline scripts, fixtures, review doc, and ledger update after validation.
- forbidden_changes: Other skills, repo-level validators, unrelated docs, or unrelated ledger rows.
- validation_plan: Skill DoD, skill script contract, local check script, repo strict validation, docs count, repo boundaries, adversarial tests, doc-factory check, global script checks, and diff whitespace check.
- merge_criteria: Local validation green, PR ready, Quality Gates green, squash merge, branch cleanup, and updated `main`.

## Local Evidence

- `bash skills/runtime-routing/scripts/check.sh`: `runtime-routing check passed: valid=2 invalid=10`.
- `python3 -B scripts/validate-skill-dod.py --skill runtime-routing`: `skill=runtime-routing dod=pass errors=0`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill runtime-routing`: `skills_with_scripts=1 warnings=0 errors=0`.
- `python3 -B scripts/validate-skills.py --strict`: `skills=600 warnings=0 errors=0`.
- `python3 -B scripts/count-components.py --check-docs`: `skills=600 agents=261 commands=267 prompts=256 components=1384`.
- `bash scripts/check-repo-boundaries.sh`: `Repo boundaries OK`.
- `python3 -B scripts/qa/run-adversarial-tests.py`: `summary: passed=11 failed=0 total=11`.
- `bash scripts/doc-factory/check.sh`: `OK: doc-factory deterministic smoke check passed`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks`: `skills_with_scripts=116 warnings=0 errors=0`.
- `git diff --check`: pass with no output.

## Guardian Decision

- status: pass
- decision: Authorize PR creation because the skill now has deterministic assets, evals, offline scripts, fixtures, review doc, reconciled ledger row, and passing local validation evidence.
- remaining_risks: Live runtime capabilities require executed checks in the actual target runtime.
