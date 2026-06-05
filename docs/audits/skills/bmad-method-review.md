# Skill Review: bmad-method

Date: 2026-06-05
Reviewer: Codex multiagent hardening pass
Status: reviewed and improved
Severity: P1

## Intended Purpose

`bmad-method` teaches and applies BMAD as a deterministic documentation-first lifecycle: route phases, assign personas, enforce artifact order, decide Quick Flow eligibility, and block Phase 4 until the readiness gate allows it. [CÓDIGO] The hardened skill must avoid claiming unavailable BMAD runtime helpers, must not use network or non-deterministic sampling by default, and must validate output packets offline.

## Spoke Reports

| Spoke | Status | Findings | Coverage Gaps | Recommended Changes | Risk |
|---|---|---|---|---|---|
| Coordinator | complete | [CONFIG] One Phase 1 skill selected after `assembly-skill`; branch created from `origin/main`. | [CONFIG] None. | [CONFIG] Keep branch and PR scoped to `bmad-method`. | [CONFIG] Low if no other skill is touched. |
| Determinism Auditor | complete | [CÓDIGO] Pre-hardening DoD failed with missing `assets/`, scaffold examples, root-list evals, and absent local script evidence. [CÓDIGO] `SKILL.md` referenced unavailable scripts, templates, workflow prompts, and persona files as if they were local. [CÓDIGO] Guidance contained uncontrolled web/research and non-deterministic sampling language. | [CÓDIGO] No local assets enforced persona routing, artifact chain, readiness gate vocabulary, Quick Flow policy, packet shape, or source policy. | [CONFIG] Add deterministic assets, offline validator fixtures, stable eval cases, local examples, and conditional language for optional target-project BMAD helpers. | [INFERENCIA] High before hardening because users could receive false confidence or premature Phase 4 approval. |
| Eval Designer | complete | [CÓDIGO] Evals were not in DoD `cases` shape. | [CÓDIGO] Missing greenfield, brownfield, PRD, architecture, story generation, gate fail, persona routing, conflict, missing context, no premature implementation, Quick Flow, and false-positive coverage. | [CONFIG] Convert evals to 12 deterministic cases with `expected_checks`, positive/negative expectations, and false-positive routing. | [INFERENCIA] Medium after hardening, pending full PR gates. |
| Guardian | complete | [CÓDIGO] Ledger row was `pending`; review doc missing. [CÓDIGO] Skill-local script evidence was absent before hardening. | [CONFIG] Full PR gates still required before merge. | [CONFIG] Block ledger closure until assets, evals, examples, scripts, review doc, DoD, and script checks pass. | [INFERENCIA] Low after per-skill validation, pending PR gates. |

## Hardening Brief

- [CONFIG] Add deterministic BMAD assets for persona routing, artifact chain, readiness gate policy, Quick Flow policy, output packet contract, and source policy.
- [CONFIG] Add an offline packet validator and fixtures for greenfield pass, Quick Flow pass, and gate-fail rejection.
- [CONFIG] Replace scaffold examples, README, output templates, agents, prompts, knowledge, and evals with BMAD-specific deterministic content.
- [CONFIG] Convert optional BMAD runtime scripts/templates/personas/checklists into verified target-project helpers rather than claimed local files.
- [CONFIG] Replace non-deterministic sampling guidance with stable document-order or path-order sampling.

## Improvement Applied

| Area | Change |
|---|---|
| `SKILL.md` | [CÓDIGO] Added `When to Activate`, deterministic guardrails, verified-helper rule, PASS-only Phase 4 entry, local asset usage, and validation command. |
| `README.md` | [CÓDIGO] Replaced scaffold text with activation boundaries, deterministic resources, and local checks. |
| `assets/` | [CÓDIGO] Added persona matrix, artifact chain, readiness gate policy, Quick Flow policy, packet contract, source policy, README, and manifest. |
| `scripts/` | [CÓDIGO] Added `validate_bmad_packet.py`, fixture contract, pass/fail packet fixtures, and `check.sh`. |
| `evals/evals.json` | [CÓDIGO] Replaced root-list evals with twelve DoD `cases` and explicit expected checks. |
| `examples/*` | [CÓDIGO] Added realistic BMAD greenfield input and evidence-tagged output packet. |
| `agents/*` and `prompts/*` | [CÓDIGO] Specialized roles around BMAD phase routing, artifact chain, gate enforcement, and Quick Flow eligibility. |
| `templates/*` | [CÓDIGO] Replaced generic templates with BMAD output templates and removed remote network dependencies. |
| `knowledge/*` and `references/*` | [CÓDIGO] Added deterministic BMAD guidance and conditioned external helper references on verified target-project files. |

## Per-Skill No-Regression Check

Observed on 2026-06-05:

```bash
python3 -m json.tool skills/bmad-method/assets/manifest.json
python3 -m json.tool skills/bmad-method/evals/evals.json
bash skills/bmad-method/scripts/check.sh
python3 -B scripts/validate-skill-dod.py --skill bmad-method
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill bmad-method
python3 -B scripts/validate-skills.py --strict
```

Results:

- [CÓDIGO] Asset and eval JSON parsed successfully.
- [CÓDIGO] `OK: bmad-method packets validated`
- [CÓDIGO] `skill=bmad-method dod=pass errors=0`
- [CÓDIGO] `skills_with_scripts=1 warnings=0 errors=0`
- [CÓDIGO] `skills=600 warnings=0 errors=0`

## PR Gate Check

Observed on 2026-06-05:

```bash
python3 scripts/validate-skills.py --strict
python3 scripts/validate-skill-scripts.py --strict --run-checks
bash scripts/doc-factory/check.sh
python3 scripts/count-components.py --check-docs
bash scripts/check-repo-boundaries.sh
python3 scripts/validate-runtime-instructions.py
bash scripts/adapt.sh all
python3 scripts/qa/run-adversarial-tests.py
python3 scripts/qa/run-confidence-fp-tests.py
python3 scripts/post_annotations.py --validate-only references/schemas/annotations.example.json
bash scripts/generate-pristino-index.sh
git diff --check
git diff --cached --check
```

Results:

- [CÓDIGO] `skills=600 warnings=0 errors=0`
- [CÓDIGO] `skills_with_scripts=34 warnings=0 errors=0`
- [CÓDIGO] `OK: doc-factory deterministic smoke check passed`
- [CÓDIGO] `skills=600 agents=261 commands=267 prompts=256 components=1384`
- [CÓDIGO] `Repo boundaries OK`
- [CÓDIGO] `runtime instructions: passed`
- [CÓDIGO] `summary: passed=11 failed=0 total=11`
- [CÓDIGO] `OK: confidence calibration, stratified sampling, and FP-criteria checks passed`
- [CÓDIGO] `VALID: 2 annotation(s) conform to annotations.schema.json`
- [CÓDIGO] `shellcheck not installed; skipping shell lint`
- [CÓDIGO] `workflow-local-pass`

## Decision

[CONFIG] Improved now and ready for full PR validation.

## Ledger Completion 2026-06-05

- [CONFIG] Ledger status may be set to `dod-complete` after per-skill DoD and script checks pass, with PR merge still gated by full-repo validation.
