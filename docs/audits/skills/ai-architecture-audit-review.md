# ai-architecture-audit Review

## SpokeReport — Determinism Auditor
- status: warn
- findings:
  - DoD base failed because `assets/` was missing, examples were scaffold-generated, and `evals/evals.json` lacked a `cases` object. [CÓDIGO]
  - Agents, prompts, templates, and knowledge graph contained generic scaffold guidance. [CÓDIGO]
  - References were domain-rich, but the skill lacked an offline report contract and deterministic validator. [CÓDIGO]
- coverage_gaps:
  - No machine-checkable evidence, severity, six-dimension, remediation, or roadmap contract. [CÓDIGO]
  - No deterministic negative fixtures for missing evidence, invalid severity, missing dimension, missing remediation, or missing threshold. [CÓDIGO]
- recommended_changes:
  - Add audit-dimension, severity, evidence, remediation, and report-contract assets. [CONFIG]
  - Add offline validator and fixtures for complete and limited audits. [CONFIG]
- risk: an audit report can look authoritative while inventing evidence or omitting required dimensions. [INFERENCIA]

## SpokeReport — Eval Designer
- status: pass
- findings:
  - Added 10 deterministic eval cases covering standard audit, GenAI security, pre-production degradation, no-code limitation, false-positive design request, evidence absence, invalid severity, remediation gaps, anti-pattern method, and script contract. [CÓDIGO]
- coverage_gaps:
  - Future domain variants should add fixtures before changing severity or evidence policy. [INFERENCIA]
- recommended_changes:
  - Keep `evals/evals.json` aligned with the validator and assets. [CONFIG]
- risk: broad AI architecture wording can over-activate on design/implementation requests. [INFERENCIA]

## SpokeReport — Script Engineer
- status: pass
- findings:
  - Added `scripts/validate_ai_architecture_audit_report.py`, `scripts/check.sh`, 2 valid fixtures, and 5 invalid fixtures. [CÓDIGO]
  - Validator enforces D1-D6 coverage, concrete evidence per finding, severity taxonomy, quality attribute thresholds, anti-pattern detection method, security controls, technical debt fields, roadmap references, and remediation DoD. [CÓDIGO]
- coverage_gaps:
  - The script validates the JSON audit packet, not live static-analysis tooling. [CÓDIGO]
- recommended_changes:
  - Treat live code/metric scans as evidence producers feeding the validated packet. [CONFIG]
- risk: live audit sources vary by client; JSON contract remains the stable validation surface. [INFERENCIA]

## HardeningBrief
- skill: ai-architecture-audit
- scope_allowed:
  - `skills/ai-architecture-audit/**` [CONFIG]
  - `docs/audits/skills/ai-architecture-audit-review.md` [CONFIG]
  - `docs/audits/skill-review-ledger.csv` row for `ai-architecture-audit` only after validation evidence exists. [CONFIG]
- required_changes:
  - Add deterministic assets, evals, examples, scripts, fixtures, specialized prompts/agents/templates/knowledge, and review doc. [CONFIG]
  - Validate offline and repository-wide before PR. [CONFIG]
- forbidden_changes:
  - Do not touch other skills. [CONFIG]
  - Do not implement remediation code; audit only. [CONFIG]
  - Do not mark `dod-complete` before local evidence is available. [CONFIG]
- validation_plan:
  - `bash skills/ai-architecture-audit/scripts/check.sh` [CONFIG]
  - `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill ai-architecture-audit` [CONFIG]
  - `python3 -B scripts/validate-skill-dod.py --skill ai-architecture-audit` [CONFIG]
  - repository-level validation suite before PR. [CONFIG]
- merge_criteria:
  - All local validations pass. [CONFIG]
  - PR Quality Gates pass. [CONFIG]
  - Squash merge only after green CI. [CONFIG]

## Local Evidence
- `bash skills/ai-architecture-audit/scripts/check.sh` passed with 2 valid fixtures accepted and 5 invalid fixtures rejected. [CÓDIGO]
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill ai-architecture-audit` passed with `skills_with_scripts=1 warnings=0 errors=0`. [CÓDIGO]
- `python3 -B scripts/validate-skill-dod.py --skill ai-architecture-audit` passed with `skill=ai-architecture-audit dod=pass errors=0`. [CÓDIGO]

## Guardian Decision
- pass for local skill-level DoD; proceed to repository validation before PR. [CÓDIGO]
