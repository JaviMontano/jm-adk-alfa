# ai-design-patterns Review

## SpokeReport - Ledger Auditor
- status: pass [CÓDIGO]
- findings:
  - Ledger row existed for `ai-design-patterns` with status `pending` before hardening. [CÓDIGO]
  - Review doc did not exist before this pass. [CÓDIGO]
- coverage_gaps:
  - No DoD evidence was recorded for this skill before the current branch. [CÓDIGO]
- recommended_changes:
  - Close only the `ai-design-patterns` ledger row after local validation evidence is available. [CONFIG]
- risk: marking `dod-complete` without validation would break the one-skill hardening contract. [CONFIG]

## SpokeReport - Determinism Auditor
- status: warn [CÓDIGO]
- findings:
  - Initial DoD failed because `assets/` was missing, examples retained scaffold text, and `evals/evals.json` did not expose a `cases` list. [CÓDIGO]
  - The skill body had useful AI design pattern references, but agents, prompts, knowledge, templates, examples, and evals were generic support files. [CÓDIGO]
  - No offline contract existed for pattern catalog membership, anti-pattern remediation, evidence ids, dependency policy, tactic categories, or roadmap exit criteria. [CÓDIGO]
- coverage_gaps:
  - Live model performance and external MLOps tool behavior remain outside this offline packet validator. [CÓDIGO]
- recommended_changes:
  - Add deterministic assets and local validator for AI design pattern selection reports. [CONFIG]
  - Require explicit evidence, closed pattern names, dependency checks, and roadmap exit criteria. [CONFIG]
- risk: AI pattern advice can overfit fashionable patterns unless dependency and avoid/defer decisions are evidence-backed. [INFERENCIA]

## SpokeReport - Eval Designer
- status: pass [CÓDIGO]
- findings:
  - Added 10 deterministic eval cases covering fraud modernization, shadow/canary rollout, avoided feature-store overengineering, unknown patterns, missing evidence, missing dependencies, roadmap gaps, false-positive weather/UI prompts, and script validation. [CÓDIGO]
- coverage_gaps:
  - The evals validate scenario behavior and output contracts, not live serving infrastructure. [CÓDIGO]
- recommended_changes:
  - Keep false-positive activation cases in evals so generic UI or weather prompts do not trigger this skill. [CONFIG]
- risk: broad "pattern" language can cause false activation unless the AI-system scope remains explicit. [INFERENCIA]

## SpokeReport - Script Engineer
- status: pass [CÓDIGO]
- findings:
  - Added `scripts/validate_ai_design_patterns_report.py`, `scripts/check.sh`, 2 valid fixtures, and 7 invalid fixtures. [CÓDIGO]
  - Validator enforces schema, evidence ids, closed pattern catalog, priority values, anti-pattern remediation pattern, tactic category, dependency policy, validation checks, and roadmap exit criteria. [CÓDIGO]
- coverage_gaps:
  - The script validates deterministic report packets, not runtime ML quality or cloud platform state. [CÓDIGO]
- recommended_changes:
  - Treat external architecture diagrams and MLOps inventory as evidence inputs to the packet, not as live dependencies of the validator. [CONFIG]
- risk: runtime topology can drift after the packet is produced, so the report remains a decision artifact rather than a live system monitor. [INFERENCIA]

## HardeningBrief
- skill: ai-design-patterns [CONFIG]
- scope_allowed:
  - `skills/ai-design-patterns/**` [CONFIG]
  - `docs/audits/skills/ai-design-patterns-review.md` [CONFIG]
  - `docs/audits/skill-review-ledger.csv` row for `ai-design-patterns` only after local evidence exists. [CONFIG]
- required_changes:
  - Add deterministic assets, eval cases, examples, scripts, fixtures, specialized prompts/agents/templates/knowledge, and review doc. [CONFIG]
  - Validate offline and repository-wide before PR. [CONFIG]
- forbidden_changes:
  - Do not touch other skills. [CONFIG]
  - Do not recommend catalog-external patterns as valid outputs. [CONFIG]
  - Do not mark `dod-complete` before evidence, review doc, and validations pass. [CONFIG]
- validation_plan:
  - `bash skills/ai-design-patterns/scripts/check.sh` [CONFIG]
  - `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill ai-design-patterns` [CONFIG]
  - `python3 -B scripts/validate-skill-dod.py --skill ai-design-patterns` [CONFIG]
  - repository-level validation suite before PR. [CONFIG]
- merge_criteria:
  - All local validations pass. [CONFIG]
  - PR Quality Gates pass. [CONFIG]
  - Squash merge only after green CI. [CONFIG]

## Local Evidence
- `bash skills/ai-design-patterns/scripts/check.sh` passed with 2 valid fixtures accepted and 7 invalid fixtures rejected. [CÓDIGO]
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill ai-design-patterns` passed with `skills_with_scripts=1 warnings=0 errors=0`. [CÓDIGO]
- `python3 -B scripts/validate-skill-dod.py --skill ai-design-patterns` passed with `skill=ai-design-patterns dod=pass errors=0`. [CÓDIGO]
- `python3 -B scripts/validate-skills.py --strict` passed with `skills=600 warnings=0 errors=0`. [CÓDIGO]
- `python3 -B scripts/count-components.py --check-docs` passed with `skills=600`, `agents=261`, `commands=267`, `prompts=256`, `components=1384`. [CÓDIGO]
- `bash scripts/check-repo-boundaries.sh` passed with `Repo boundaries OK`. [CÓDIGO]
- `python3 -B scripts/qa/run-adversarial-tests.py` passed with `summary: passed=11 failed=0 total=11`. [CÓDIGO]
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks` passed with `skills_with_scripts=86 warnings=0 errors=0`. [CÓDIGO]
- `bash scripts/doc-factory/check.sh` passed with `OK: doc-factory deterministic smoke check passed`. [CÓDIGO]
- `git diff --check` passed with no output. [CÓDIGO]

## Guardian Decision
- pass for local skill-level and repository-level validation; proceed to PR creation and Quality Gates. [CÓDIGO]
