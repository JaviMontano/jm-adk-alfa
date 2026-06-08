# mcp-engineering Review

## SpokeReport - Determinism Auditor

- status: pass
- findings: Initial DoD failed because `assets/` was missing and evals lacked `assets` and `deterministic_scripts`. Public files retained scaffold headers.
- coverage_gaps: No offline oracle existed for scope mismatch, literal secrets, missing typed error categories, retryability mistakes, retry policy owned by the model, built-in false positives, or incomplete secret remediation.
- recommended_changes: Add deterministic assets, specialized eval cases, examples, prompts, agents, template, knowledge, offline scripts, fixtures, review doc, and ledger update.
- risk: Without these changes, an MCP integration could ship with leaked credentials, ambiguous retry behavior, or an unnecessary server where a built-in tool would suffice.

## SpokeReport - Eval Designer

- status: pass
- findings: Replaced generic eval checks with 11 deterministic cases covering team config, typed errors, personal scope, leaked-secret remediation, explicit triggers, minimal actionable inputs, false positives, literal secret rejection, generic error rejection, and upgrade safety.
- coverage_gaps: None remaining for the DoD hardening scope.
- recommended_changes: Keep evals tied to `assets`, `deterministic_scripts`, `scope_policy`, `secret_policy`, `typed_error_contract`, `client_retry_policy`, and `builtin_review`.
- risk: Future edits could weaken guarantees if evals stop testing scope and retry ownership together.

## SpokeReport - Script Engineer

- status: pass
- findings: Added `scripts/validate_mcp_engineering.py`, `scripts/check.sh`, 2 valid fixtures, and 8 invalid mutation fixtures.
- coverage_gaps: The script validates structured JSON MCP engineering reports, not arbitrary prose-only Markdown.
- recommended_changes: Use the JSON contract whenever MCP config and typed error behavior must be checked offline.
- risk: Markdown-only deliverables still require Guardian review against the same deterministic contract.

## HardeningBrief

- skill: mcp-engineering
- scope_allowed: `skills/mcp-engineering/**`, `docs/audits/skills/mcp-engineering-review.md`, and the `mcp-engineering` ledger row.
- required_changes: Assets, examples, eval cases, prompts, agents, template, knowledge, offline scripts, fixtures, review doc, and ledger update.
- forbidden_changes: Other skills, adapters generated from canonical files, repo-level validators, unrelated docs, or unrelated ledger rows.
- validation_plan: Skill DoD, skill script contract, local check script, repo strict validation, docs count, repo boundaries, adversarial tests, doc-factory check, adapter freshness, global script checks, and diff whitespace check.
- merge_criteria: Local validation green, PR ready, Quality Gates green, squash merge, branch cleanup, and updated `main`.

## Local Evidence

- `bash skills/mcp-engineering/scripts/check.sh`: `mcp-engineering check passed: valid=2 invalid=8`.
- `python3 -B scripts/validate-skill-dod.py --skill mcp-engineering`: `skill=mcp-engineering dod=pass errors=0`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill mcp-engineering`: `skills_with_scripts=1 warnings=0 errors=0`.
- `python3 -B scripts/validate-skills.py --strict`: `skills=600 warnings=0 errors=0`.
- `python3 -B scripts/count-components.py --check-docs`: `skills=600 agents=261 commands=267 prompts=256 components=1384`.
- `bash scripts/check-repo-boundaries.sh`: `Repo boundaries OK`.
- `python3 -B scripts/qa/run-adversarial-tests.py`: `summary: passed=11 failed=0 total=11`.
- `bash scripts/doc-factory/check.sh`: `OK: doc-factory deterministic smoke check passed`.
- `bash scripts/adapt.sh all` plus adapter diff check: `adapter freshness OK`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks`: `skills_with_scripts=107 warnings=0 errors=0`.
- `git diff --check`: pass with no output.

## Guardian Decision

- status: pass
- decision: Authorize PR creation because the ledger row is updated and all local checks passed.
- remaining_risks: Prose-only MCP integration proposals require human review against the JSON contract before they can be treated as deterministic evidence.
