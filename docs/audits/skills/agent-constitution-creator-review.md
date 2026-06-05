# Skill Review: agent-constitution-creator

Date: 2026-06-05
Reviewer: Codex multiagent hardening pass
Status: reviewed and improved
Severity: P1

## Intended Purpose

`agent-constitution-creator` creates deterministic `agents/{id}/agent.md` constitutions for multi-agent ecosystems. [CÓDIGO] The hardened skill must preserve 22 required fields, enforce registry-only tools, block invented authority, require escalation context, and validate generated constitutions offline before delivery.

## Spoke Reports

| Spoke | Status | Findings | Coverage Gaps | Recommended Changes | Risk |
|---|---|---|---|---|---|
| Coordinator | complete | [CONFIG] One Phase 1 skill selected after `ux-writing`; branch created from `origin/main`. | [CONFIG] None. | [CONFIG] Keep branch and PR scoped to `agent-constitution-creator`. | [CONFIG] Low if scope remains isolated. |
| Determinism Auditor | complete | [CÓDIGO] Pre-hardening DoD failed with 5 errors: missing assets, scaffold examples, malformed eval shape, and no script contract. [CÓDIGO] Frontmatter contained evidence tags in metadata and templates used remote fonts/free date tokens. | [CÓDIGO] No offline schema, authority policy, fixtures, or validator enforced the 22-field constitution contract. | [CONFIG] Add assets, schema, no-invention policy, deterministic script, fixtures, offline templates, and valid frontmatter. | [INFERENCIA] Medium-high before hardening. |
| Eval Designer | complete | [CÓDIGO] Evals were a raw seven-case activation array. | [CÓDIGO] Missing cases for 22 fields, authority boundaries, registry-only tools, escalation, evidence tags, interview mode, conflicting authority, false positives, no invented permissions, and overlap detection. | [CONFIG] Convert evals to DoD `cases` with concrete expected checks. | [INFERENCIA] High before hardening because incomplete constitutions could pass. |
| Guardian | complete | [CÓDIGO] Ledger row was `pending`; focused DoD failed before changes. | [CÓDIGO] No review doc existed and script checks only passed because no scripts existed. | [CONFIG] Block ledger closure until assets, evals, examples, scripts, review doc, and DoD pass. | [INFERENCIA] Low after per-skill validation, pending PR gates. |

## Hardening Brief

- [CONFIG] Replace scaffold README, examples, evals, prompts, agents, templates, and knowledge with constitution-specific deterministic contracts.
- [CONFIG] Add `assets/agent-constitution-template.md`, `assets/agent-constitution-schema.json`, `assets/authority-policy.json`, and `assets/constitution-checklist.md`.
- [CONFIG] Add `scripts/validate_agent_constitution.py`, JSON fixture metadata, pass/fail Markdown fixtures, and `scripts/check.sh`.
- [CONFIG] Convert evals to ten DoD `cases` covering required fields, authority boundaries, tool registry, escalation, evidence tags, missing context, conflicts, false positives, no invented permissions, and overlap detection.
- [CONFIG] Remove remote Google Fonts dependency and replace `{{DATE}}` with caller-provided `{{CONSTITUTION_DATE}}`.
- [CONFIG] Keep write/edit capability only for explicit `agents/{id}/agent.md` file updates; otherwise return Markdown.

## Improvement Applied

| Area | Change |
|---|---|
| `SKILL.md` | [CÓDIGO] Fixed YAML metadata, added `When to Activate`, deterministic contract, assets, scripts, no-invention policy, interview mode, and validation gate. |
| `README.md` | [CÓDIGO] Replaced scaffold text with activation, required inputs, resources, local gates, and output contract. |
| `assets/` | [CÓDIGO] Added template, schema, authority policy, checklist, README, and manifest. |
| `scripts/` | [CÓDIGO] Added offline constitution validator, fixture contract, valid/invalid fixtures, and `check.sh`. |
| `evals/evals.json` | [CÓDIGO] Replaced root-list evals with ten DoD cases and required expected checks. |
| `examples/*` | [CÓDIGO] Added realistic customer-intake constitution input and output. |
| `agents/*` and `prompts/*` | [CÓDIGO] Specialized execution, support, guardian, routing, quick, and deep modes around the deterministic contract. |
| `templates/*` | [CÓDIGO] Replaced generic templates and removed remote network dependency. |
| `knowledge/*` and `references/*` | [CÓDIGO] Added field-contract, authority, evidence, and anti-pattern guidance. |

## Per-Skill No-Regression Check

Observed on 2026-06-05:

```bash
python3 -m json.tool skills/agent-constitution-creator/assets/manifest.json
python3 -m json.tool skills/agent-constitution-creator/assets/agent-constitution-schema.json
python3 -m json.tool skills/agent-constitution-creator/assets/authority-policy.json
python3 -m json.tool skills/agent-constitution-creator/evals/evals.json
bash skills/agent-constitution-creator/scripts/check.sh
python3 -B scripts/validate-skill-dod.py --skill agent-constitution-creator
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill agent-constitution-creator
python3 -B scripts/validate-skills.py --strict
```

Results:

- [CÓDIGO] `manifest-json-ok`
- [CÓDIGO] `schema-json-ok`
- [CÓDIGO] `policy-json-ok`
- [CÓDIGO] `evals-json-ok`
- [CÓDIGO] `OK: agent-constitution-creator validator fixtures passed`
- [CÓDIGO] `skill=agent-constitution-creator dod=pass errors=0`
- [CÓDIGO] `skills_with_scripts=1 warnings=0 errors=0`
- [CÓDIGO] `skills=600 warnings=0 errors=0`

## PR Gate Check

Observed on 2026-06-05:

```bash
python3 -B scripts/validate-skills.py --strict
python3 -B scripts/count-components.py --check-docs
python3 -B scripts/validate-mcp-config.py
python3 -B scripts/check-devkit-readiness.py
bash scripts/check-repo-boundaries.sh
python3 -B scripts/qa/run-adversarial-tests.py
python3 -B scripts/validate-skill-scripts.py --strict --run-checks
bash scripts/doc-factory/check.sh
bash scripts/adapt.sh all
git diff --quiet -- AGENTS.md GEMINI.md .agent/rules/GEMINI.md .agent/ARCHITECTURE.md .agent/skills_index.json .github/copilot-instructions.md .cursorrules .windsurfrules
bash scripts/generate-pristino-index.sh
git diff --quiet -- PRISTINO-INDEX.md
git diff --check
```

Results:

- [CÓDIGO] `skills=600 warnings=0 errors=0`
- [CÓDIGO] `skills=600 agents=261 commands=267 prompts=256 components=1384`
- [CÓDIGO] `mcp config: passed`
- [CÓDIGO] `devkit readiness: passed`
- [CÓDIGO] `Repo boundaries OK`
- [CÓDIGO] `summary: passed=11 failed=0 total=11`
- [CÓDIGO] `skills_with_scripts=32 warnings=0 errors=0`
- [CÓDIGO] `OK: doc-factory deterministic smoke check passed`
- [CÓDIGO] Runtime adapters refreshed after CI exposed stale `.agent/skills_index.json` output.
- [CÓDIGO] `PRISTINO-INDEX.md` regenerated after CI exposed stale generated index output.
- [CÓDIGO] `git diff --check` produced no output

## Decision

[CONFIG] Improved now and ready for full PR validation.

## Ledger Completion 2026-06-05

- [CONFIG] Ledger status may be set to `dod-complete` after per-skill DoD and script checks pass, with PR merge still gated by full-repo validation.
