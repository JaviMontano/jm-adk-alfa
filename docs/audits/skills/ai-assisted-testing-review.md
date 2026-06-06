# ai-assisted-testing Review

## SpokeReport - Determinism Auditor
- status: warn
- findings:
  - DoD base failed because `assets/` was missing. [CÓDIGO]
  - Existing examples, eval cases, agents, prompts, templates, and knowledge were hardened for AI-generated tests, fuzzing, mutation testing, and coverage optimization. [CÓDIGO]
  - The original skill had no offline contract for distinguishing proposed, generated, and executed tests. [CÓDIGO]
- coverage_gaps:
  - No machine-checkable test-plan packet existed for evidence, oracles, bounded fuzzing, mutation baseline, or coverage targets. [CÓDIGO]
  - No fixtures existed for invalid missing evidence, missing oracle, unsafe fuzzing, missing mutation baseline, or weak coverage targets. [CÓDIGO]
- recommended_changes:
  - Add deterministic assets and a local validator for AI Assisted Testing plans. [CONFIG]
  - Require candidate tests to include target, rationale, oracle, status, and evidence references. [CONFIG]
- risk: generated test recommendations can appear complete while inventing targets or claiming execution without evidence. [INFERENCIA]

## SpokeReport - Eval Designer
- status: pass
- findings:
  - Added 10 deterministic eval cases covering unit plans, fuzzing, mutation testing, coverage optimization, false-positive activation, no-evidence degradation, missing oracle, unsafe fuzzing, missing mutation baseline, and script validation. [CÓDIGO]
- coverage_gaps:
  - Live project-specific test frameworks remain outside this skill contract. [INFERENCIA]
- recommended_changes:
  - Keep the skill focused on reviewable test plans and candidate tests unless project execution evidence is supplied. [CONFIG]
- risk: broad testing prompts can over-activate on unrelated quality or weather requests without explicit activation boundaries. [INFERENCIA]

## SpokeReport - Script Engineer
- status: pass
- findings:
  - Added `scripts/validate_ai_assisted_testing_plan.py`, `scripts/check.sh`, 2 valid fixtures, and 5 invalid fixtures. [CÓDIGO]
  - Validator enforces schema, evidence IDs, candidate-test oracles, execution evidence, bounded fuzzing, mutation baseline, coverage targets, and required validation checks. [CÓDIGO]
- coverage_gaps:
  - The script validates the assisted-testing plan packet, not live test execution in arbitrary user repositories. [CÓDIGO]
- recommended_changes:
  - Treat live test execution outputs as evidence inputs to the packet. [CONFIG]
- risk: project-specific frameworks vary; the packet contract is the stable validation boundary. [INFERENCIA]

## HardeningBrief
- skill: ai-assisted-testing
- scope_allowed:
  - `skills/ai-assisted-testing/**` [CONFIG]
  - `docs/audits/skills/ai-assisted-testing-review.md` [CONFIG]
  - `docs/audits/skill-review-ledger.csv` row for `ai-assisted-testing` only after local evidence exists. [CONFIG]
- required_changes:
  - Add deterministic assets, eval cases, examples, scripts, fixtures, specialized prompts/agents/templates/knowledge, and review doc. [CONFIG]
  - Validate offline and repository-wide before PR. [CONFIG]
- forbidden_changes:
  - Do not touch other skills. [CONFIG]
  - Do not claim generated tests passed without execution evidence. [CONFIG]
  - Do not mark `dod-complete` before local validation evidence is available. [CONFIG]
- validation_plan:
  - `bash skills/ai-assisted-testing/scripts/check.sh` [CONFIG]
  - `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill ai-assisted-testing` [CONFIG]
  - `python3 -B scripts/validate-skill-dod.py --skill ai-assisted-testing` [CONFIG]
  - repository-level validation suite before PR. [CONFIG]
- merge_criteria:
  - All local validations pass. [CONFIG]
  - PR Quality Gates pass. [CONFIG]
  - Squash merge only after green CI. [CONFIG]

## Local Evidence
- `bash skills/ai-assisted-testing/scripts/check.sh` passed with 2 valid fixtures accepted and 5 invalid fixtures rejected. [CÓDIGO]
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill ai-assisted-testing` passed with `skills_with_scripts=1 warnings=0 errors=0`. [CÓDIGO]
- `python3 -B scripts/validate-skill-dod.py --skill ai-assisted-testing` passed with `skill=ai-assisted-testing dod=pass errors=0`. [CÓDIGO]

## Guardian Decision
- pass for local skill-level DoD; proceed to repository validation before PR. [CÓDIGO]
