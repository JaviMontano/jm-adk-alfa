# environment-detection Review

## SpokeReport — Determinism Auditor
- status: warn
- findings:
  - DoD base failed because `assets/` was missing, examples were scaffold-generated, and `evals/evals.json` was a list instead of a `cases` object. [CÓDIGO]
  - README, agents, prompts, templates, and knowledge files contained generic scaffold text or non-JM Labs/remote template assumptions. [CÓDIGO]
  - Original instructions allowed broad IDE/model detection without an offline report contract or deterministic evidence policy. [CÓDIGO]
- coverage_gaps:
  - No explicit rejection of network/time/random/account-state detection evidence. [CÓDIGO]
  - No deterministic fixture coverage for conflicting host markers, unknown model budget, light-tier loading, or full-triad capability requirements. [CÓDIGO]
- recommended_changes:
  - Add signal, capability, model-tier, loading, and report-contract assets. [CONFIG]
  - Add an offline JSON validator with positive and negative fixtures. [CONFIG]
  - Replace generic evals/examples/prompts/templates/knowledge with environment-specific contracts. [CONFIG]
- risk: false confident environment detection can select the wrong orchestration mode and overload context. [INFERENCIA]

## SpokeReport — Eval Designer
- status: pass
- findings:
  - Added 10 deterministic eval cases covering Codex, Claude Code, Cursor, Copilot, false positive, conflicts, unknown model budget, light tier, rejected network evidence, and script fixtures. [CÓDIGO]
- coverage_gaps:
  - Future hosts should add both a policy row and a matching fixture before activation guidance changes. [INFERENCIA]
- recommended_changes:
  - Keep host mapping table and validator fixtures synchronized. [CONFIG]
- risk: new IDE hosts could otherwise inherit unsafe defaults. [INFERENCIA]

## SpokeReport — Script Engineer
- status: pass
- findings:
  - Added `scripts/validate_environment_detection_report.py` and `scripts/check.sh` for offline report validation. [CÓDIGO]
  - Added valid Codex, valid Claude Code, valid unknown/warn, and five invalid fixtures. [CÓDIGO]
- coverage_gaps:
  - The script validates the report contract, not live IDE discovery commands. [CÓDIGO]
- recommended_changes:
  - Treat live discovery as an input producer; keep the JSON report as the testable artifact. [CONFIG]
- risk: live environment APIs can vary, so the report contract is the stable validation boundary. [INFERENCIA]

## HardeningBrief
- skill: environment-detection
- scope_allowed:
  - `skills/environment-detection/**` [CONFIG]
  - `docs/audits/skills/environment-detection-review.md` [CONFIG]
  - `docs/audits/skill-review-ledger.csv` row for `environment-detection` only after validation evidence exists. [CONFIG]
- required_changes:
  - Add deterministic assets, evals, examples, scripts, fixtures, specialized prompts/agents/templates/knowledge, and review doc. [CONFIG]
  - Validate offline and repository-wide before PR. [CONFIG]
- forbidden_changes:
  - Do not touch other skills. [CONFIG]
  - Do not use network/current-time/random evidence for report validation. [CONFIG]
  - Do not mark `dod-complete` before local evidence is available. [CONFIG]
- validation_plan:
  - `bash skills/environment-detection/scripts/check.sh` [CONFIG]
  - `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill environment-detection` [CONFIG]
  - `python3 -B scripts/validate-skill-dod.py --skill environment-detection` [CONFIG]
  - repository-level validation suite before PR. [CONFIG]
- merge_criteria:
  - All local validations pass. [CONFIG]
  - PR Quality Gates pass. [CONFIG]
  - Squash merge only after green CI. [CONFIG]

## Local Evidence
- `bash skills/environment-detection/scripts/check.sh` passed with 3 valid fixtures accepted and 5 invalid fixtures rejected. [CÓDIGO]
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill environment-detection` passed with `skills_with_scripts=1 warnings=0 errors=0`. [CÓDIGO]
- `python3 -B scripts/validate-skill-dod.py --skill environment-detection` passed with `skill=environment-detection dod=pass errors=0`. [CÓDIGO]

## Guardian Decision
- pass for local skill-level DoD; proceed to repository validation before PR. [CÓDIGO]
