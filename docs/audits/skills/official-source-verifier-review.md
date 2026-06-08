# official-source-verifier Review

## SpokeReport - Determinism Auditor

- status: pass
- findings: Initial DoD failed because `assets/` was missing, knowledge/examples/evals were generic, and no offline evidence oracle existed.
- coverage_gaps: No deterministic check existed for secondary sources marked as authority, missing accessed dates, verified claims without official evidence, authorized changes from unverified claims, or Guardian pass on blocked evidence.
- recommended_changes: Add deterministic assets, specialized eval cases, examples, prompts, agents, template, knowledge, offline scripts, fixtures, review doc, and ledger update.
- risk: Without these changes, a secondary source could be treated as authoritative and authorize repo changes without official backing.

## SpokeReport - Eval Designer

- status: pass
- findings: Replaced generic eval checks with 10 deterministic cases covering official ADK/docs decisions, GitHub CLI behavior, Agent Skills spec questions, framework migration, secondary-source rejection, missing date rejection, local-code false positive, conflicts, unverified claims, and upgrade safety.
- coverage_gaps: None remaining for the DoD hardening scope.
- recommended_changes: Keep evals tied to `assets`, `deterministic_scripts`, `official_source_priority`, `claim_evidence`, `citation_date`, `secondary_not_authority`, and `decision_traceability`.
- risk: Future edits could weaken guarantees if evals stop testing blocked unverified claims.

## SpokeReport - Script Engineer

- status: pass
- findings: Added `scripts/validate_official_source_verifier.py`, `scripts/check.sh`, 2 valid fixtures, and 8 invalid mutation fixtures.
- coverage_gaps: The script validates structured JSON official-source reports, not arbitrary prose-only Markdown.
- recommended_changes: Use the JSON contract whenever source authority and decision traceability must be checked offline.
- risk: Markdown-only verification reports still require Guardian review against the same deterministic contract.

## HardeningBrief

- skill: official-source-verifier
- scope_allowed: `skills/official-source-verifier/**`, `docs/audits/skills/official-source-verifier-review.md`, and the `official-source-verifier` ledger row.
- required_changes: Assets, examples, eval cases, prompts, agents, template, knowledge, offline scripts, fixtures, review doc, and ledger update.
- forbidden_changes: Other skills, adapters generated from canonical files, repo-level validators, unrelated docs, or unrelated ledger rows.
- validation_plan: Skill DoD, skill script contract, local check script, repo strict validation, docs count, repo boundaries, adversarial tests, doc-factory check, adapter freshness, global script checks, and diff whitespace check.
- merge_criteria: Local validation green, PR ready, Quality Gates green, squash merge, branch cleanup, and updated `main`.

## Local Evidence

- `bash skills/official-source-verifier/scripts/check.sh`: `official-source-verifier check passed: valid=2 invalid=8`.
- `python3 -B scripts/validate-skill-dod.py --skill official-source-verifier`: `skill=official-source-verifier dod=pass errors=0`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill official-source-verifier`: `skills_with_scripts=1 warnings=0 errors=0`.
- `python3 -B scripts/validate-skills.py --strict`: `skills=600 warnings=0 errors=0`.
- `python3 -B scripts/count-components.py --check-docs`: `skills=600 agents=261 commands=267 prompts=256 components=1384`.
- `bash scripts/check-repo-boundaries.sh`: `Repo boundaries OK`.
- `python3 -B scripts/qa/run-adversarial-tests.py`: `summary: passed=11 failed=0 total=11`.
- `bash scripts/doc-factory/check.sh`: `OK: doc-factory deterministic smoke check passed`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks`: `skills_with_scripts=109 warnings=0 errors=0`.
- `bash scripts/adapt.sh all`: `ADAPTER-COMPLETE` for antigravity, vscode, cursor+windsurf, and agents+gemini with no core files modified.
- `git diff --check`: pass with no output.

## Guardian Decision

- status: pass
- decision: Authorize PR creation because the skill now has deterministic assets, evals, offline scripts, fixtures, review doc, a reconciled ledger row, adapter freshness evidence, and passing local validation.
- remaining_risks: Prose-only source-verification reports require human review against the JSON contract before they can be treated as deterministic evidence.
