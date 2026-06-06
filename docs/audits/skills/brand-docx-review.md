# Skill Review: brand-docx

Date: 2026-06-05
Reviewer: Codex multiagent hardening pass
Status: reviewed and improved
Severity: P1

## Intended Purpose

`brand-docx` generates deterministic, brand-token-compliant Microsoft Word DOCX
artifacts from supplied brand configuration or explicit fallback defaults.
[CÓDIGO] It enforces real DOCX package structure, core properties, brand tokens,
table/header/footer styling, no remote assets, no unresolved placeholders, and
offline validator fixtures. [CONFIG]

## Spoke Reports

| Spoke | Status | Findings | Coverage Gaps | Recommended Changes | Risk |
|---|---|---|---|---|---|
| Coordinator | complete | [CONFIG] `brand-docx` selected after `brand-html`; branch created from `origin/main`; no open PRs. | [CONFIG] None. | [CONFIG] Keep branch and PR scoped to one skill. | [CONFIG] Low if scope remains isolated. |
| Determinism Auditor | timeout-closed | [CÓDIGO] Initial local inspection found scaffold README/examples, root-array evals, remote-font HTML template, implicit `{{DATE}}`, hidden-user config lookup, and no assets/scripts. | [CÓDIGO] Auditor subagent did not complete before timeout and was closed; local commands and other spokes reproduced the blocking evidence. | [CONFIG] Use direct validator evidence plus Eval Designer and Guardian reports for closure. | [INFERENCIA] Medium before hardening; low after validator-backed gates pass. |
| Eval Designer | complete | [CÓDIGO] Initial evals were 5 prose cases in a root array, not a DoD `cases` object. | [CÓDIGO] Missing checks for DOCX ZIP parts, Word XML, metadata/date, brand-token override, remote assets, placeholders, and HTML renamed as DOCX. | [CONFIG] Add 12 deterministic eval cases and fixture-backed validator for pass/fail DOCX contracts. | [INFERENCIA] Medium-high before hardening because prose evals could pass non-DOCX or non-tokenized output. |
| Guardian | complete | [CÓDIGO] Initial `validate-skill-dod.py --skill brand-docx` failed with 5 errors and ledger remained pending. | [CÓDIGO] Assets, eval cases, examples, review doc, and script-backed behavior evidence were absent. | [CONFIG] Block `dod-complete` until assets, examples, evals, scripts, review doc, ledger, and per-skill validations pass. | [INFERENCIA] Closure-blocking until local validation passes. |

## Hardening Brief

- [CONFIG] Add activation, DOCX package contract, fallback config, style-token
  map, evidence, and manifest assets.
- [CONFIG] Add `scripts/validate_brand_docx.py`, `scripts/check.sh`, three
  valid fixtures, and four negative fixtures.
- [CONFIG] Replace scaffold README, examples, evals, agents, prompts, templates,
  knowledge, and reference content.
- [CONFIG] Remove `Edit`, constrain `Write` to requested artifact generation,
  and keep validation deterministic/offline.
- [CONFIG] Update ledger only after per-skill validators pass.

## Improvement Applied

| Area | Change |
|---|---|
| `SKILL.md` | [CÓDIGO] Added activation routing, deterministic resources, brand config search order, DOCX output contract, token rules, package validation, dependency boundaries, and validation commands. |
| `README.md` | [CÓDIGO] Replaced scaffold text with triggers, assets, scripts, and output contract. |
| `assets/` | [CÓDIGO] Added activation policy, DOCX contract, fallback config, style-token map, evidence policy, manifest, and README. |
| `scripts/` | [CÓDIGO] Added offline DOCX package validator, check script, valid proposal/fallback/long-table fixtures, and invalid HTML-renamed, remote-asset, placeholder, and hardcoded-token fixtures. |
| `evals/evals.json` | [CÓDIGO] Replaced root-array evals with 12 `cases` covering real DOCX packages, implicit Word activation, brand-token override, fallback, metadata/date, long tables, negative fixtures, false positives, and adversarial bypass. |
| `examples/*` | [CÓDIGO] Added realistic brand-token input and DOCX validation evidence output. |
| `agents/*` and `prompts/*` | [CÓDIGO] Specialized roles around DOCX generation, package validation, token compliance, false-positive routing, and guardian blocking. |
| `templates/*` | [CÓDIGO] Replaced scaffold/remote-font/time-dependent templates with deterministic DOCX result and package templates. |
| `knowledge/*` and `references/domain-knowledge.md` | [CÓDIGO] Added DOCX package invariants, false positives, validation rules, and anti-patterns. |

## Follow-Up Gap

- [INFERENCIA] The validator proves DOCX package structure and deterministic
  XML contract features; visual rendering in Word can still vary by installed
  fonts and should be browser/Word-inspected only when the user asks for
  pixel-level fidelity.

## Ledger Completion

- [CÓDIGO] Local ledger after hardening: `54` `dod-complete`, `531` pending.
- [CÓDIGO] `brand-docx` ledger row points to this review doc and records
  `completed-brand-docx-dod`.

## PR Gate Check

- [CÓDIGO] `bash skills/brand-docx/scripts/check.sh`: `OK: brand-docx
  artifacts validated deterministically`.
- [CÓDIGO] `python3 -B scripts/validate-skill-dod.py --skill brand-docx`:
  `skill=brand-docx dod=pass errors=0`.
- [CÓDIGO] `python3 -B scripts/validate-skill-scripts.py --strict
  --run-checks --skill brand-docx`: `skills_with_scripts=1 warnings=0 errors=0`.
- [CÓDIGO] `python3 -B scripts/validate-skills.py --strict`: `skills=600
  warnings=0 errors=0`.
- [CÓDIGO] `python3 -B scripts/validate-skill-scripts.py --strict
  --run-checks`: `skills_with_scripts=48 warnings=0 errors=0`.
- [CÓDIGO] `python3 -B scripts/count-components.py --check-docs`:
  `skills=600 agents=261 commands=267 prompts=256 components=1384`.
- [CÓDIGO] `bash scripts/check-repo-boundaries.sh`: `Repo boundaries OK`.
- [CÓDIGO] `python3 -B scripts/qa/run-adversarial-tests.py`:
  `passed=11 failed=0 total=11`.
- [CÓDIGO] `python3 -B scripts/validate-runtime-instructions.py`: runtime
  instructions passed.
- [CÓDIGO] `python3 -B scripts/qa/run-confidence-fp-tests.py`: confidence
  calibration, stratified sampling, and FP-criteria checks passed.
- [CÓDIGO] `python3 -B scripts/post_annotations.py --validate-only
  references/schemas/annotations.example.json`: `VALID`.
- [CÓDIGO] `bash scripts/doc-factory/check.sh`: deterministic smoke check
  passed.
- [CÓDIGO] `python3 -B scripts/diagnose-user-context.py --dry-run`:
  `USER_CONTEXT_STATUS: ready`.
- [CÓDIGO] `python3 -B scripts/diagnose-personal-skills.py --dry-run`:
  `PERSONAL_SKILLS_STATUS: empty`.
- [CÓDIGO] `python3 -B scripts/sync-personal-skills.py --dry-run --target
  /tmp/alfa-personal-skills-target`: `files=0`.
- [CÓDIGO] `bash scripts/adapt.sh all`: regenerated mirrors with `600` skills
  indexed.
- [CÓDIGO] `bash scripts/generate-pristino-index.sh`: `Agents: 261 | Skills:
  600 | Commands: 267 | Prompts: 256 | Components: 1384`.
- [CÓDIGO] `git diff --check`: clean.
- [INFERENCIA] `shellcheck skills/brand-docx/scripts/check.sh` was skipped
  because `shellcheck` is not installed in the local environment.

## Release Packet

- [CONFIG] Scope: one active skill, `brand-docx`.
- [CONFIG] Branch: `codex/harden-brand-docx-dod-20260605`.
- [CÓDIGO] Added deterministic DOCX support through assets, scripts, fixtures,
  eval cases, examples, templates, specialized agents, review doc, and ledger
  update.
- [CONFIG] Decision: open a ready PR only after final gate rerun.

## Decision

[CONFIG] Improved now and ready for PR gate validation.
