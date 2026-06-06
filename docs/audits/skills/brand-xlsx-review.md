# Skill Review: brand-xlsx

Date: 2026-06-06
Reviewer: Codex multiagent hardening pass
Status: reviewed and improved
Severity: P1

## Intended Purpose

`brand-xlsx` generates deterministic, brand-token-compliant Microsoft Excel
XLSX artifacts from supplied brand configuration or explicit fallback defaults.
[CÓDIGO] It enforces real XLSX package structure, core properties, workbook
XML/styles, meaningful sheet names, tab colors, merged title/footer regions,
freeze panes, bounded column widths, no remote assets, no unresolved
placeholders, and offline validator fixtures. [CONFIG]

## Spoke Reports

| Spoke | Status | Findings | Coverage Gaps | Recommended Changes | Risk |
|---|---|---|---|---|---|
| Coordinator | complete | [CONFIG] `brand-xlsx` selected after `brand-docx`; branch created from `origin/main`; no open PRs. | [CONFIG] None. | [CONFIG] Keep branch and PR scoped to one skill. | [CONFIG] Low if scope remains isolated. |
| Determinism Auditor | complete | [CÓDIGO] Initial state had no delta from `origin/main`, failed DoD, retained scaffold files, hidden `~/.claude` config lookup, `{{DATE}}`, Google Fonts, legacy hardcoded colors, and no assets/scripts. | [CÓDIGO] Missing XLSX ZIP/package validator, fixtures, token-drift negative case, hidden-config isolation, fixed-date metadata, sheet names, tab colors, fills, fonts, freeze panes, filters, merged regions, footer metadata, and openpyxl/readback contract. | [CONFIG] Add XLSX validator, deterministic fixtures, assets, non-scaffold text, no hidden config, no remote/time placeholders, and keep ledger pending until gates pass. | [INFERENCIA] High before hardening because plausible spreadsheet instructions could pass without proving a real XLSX package. |
| Eval Designer | complete | [CÓDIGO] Initial evals used `skill_name` + `evals` with 5 prose cases instead of DoD `cases`. | [CÓDIGO] Missing coverage for workbook XML parts, `xl/styles.xml`, brand tokens, footer year/domain, remote relationships, renamed non-XLSX files, false positives, and adversarial bypass. | [CONFIG] Add 13 deterministic eval cases and fixture-backed validator for pass/fail XLSX contracts. | [INFERENCIA] High for false confidence before artifact-level validation. |
| Guardian | complete | [CÓDIGO] Initial `validate-skill-dod.py --skill brand-xlsx` failed with 5 errors and ledger remained pending. | [CÓDIGO] Assets, eval cases, examples, review doc, and script-backed behavior evidence were absent. | [CONFIG] Block `dod-complete` until assets, examples, evals, scripts, review doc, ledger, and per-skill validations pass. | [INFERENCIA] Closure-blocking until local validation passes. |

## Hardening Brief

- [CONFIG] Add activation, XLSX workbook contract, fallback config, style-token
  map, evidence, and manifest assets.
- [CONFIG] Add `scripts/validate_brand_xlsx.py`, `scripts/check.sh`, three
  valid fixtures, and five negative fixtures.
- [CONFIG] Replace scaffold README, examples, evals, agents, prompts, templates,
  knowledge, and reference content.
- [CONFIG] Remove `Edit`, constrain `Write` to requested artifact generation,
  and keep validation deterministic/offline.
- [CONFIG] Update ledger only after per-skill validators pass.

## Improvement Applied

| Area | Change |
|---|---|
| `SKILL.md` | [CÓDIGO] Added activation routing, deterministic resources, brand config search order, XLSX output contract, token rules, workbook validation, dependency boundaries, and validation commands. |
| `README.md` | [CÓDIGO] Replaced scaffold text with triggers, assets, scripts, and output contract. |
| `assets/` | [CÓDIGO] Added activation policy, XLSX contract, fallback config, style-token map, evidence policy, manifest, and README. |
| `scripts/` | [CÓDIGO] Added offline XLSX package validator, check script, valid report/fallback/wide-data fixtures, and invalid not-zip, missing-parts, off-token, remote-asset, and placeholder fixtures. |
| `evals/evals.json` | [CÓDIGO] Replaced prose evals with 13 `cases` covering real XLSX packages, workbook styles, token override, metadata, fallback, wide data, negative fixtures, false positives, implicit Excel activation, and adversarial bypass. |
| `examples/*` | [CÓDIGO] Added realistic brand-token input and XLSX validation evidence output. |
| `agents/*` and `prompts/*` | [CÓDIGO] Specialized roles around XLSX generation, package validation, token compliance, false-positive routing, and guardian blocking. |
| `templates/*` | [CÓDIGO] Replaced scaffold/remote-font/time-dependent templates with deterministic XLSX result and package templates. |
| `knowledge/*` and `references/domain-knowledge.md` | [CÓDIGO] Added XLSX package invariants, false positives, validation rules, and anti-patterns. |

## Follow-Up Gap

- [INFERENCIA] The validator proves XLSX package structure and deterministic XML
  contract features; visual rendering in Excel can still vary by installed
  fonts and should be inspected only when the user asks for pixel-level
  fidelity.

## Ledger Completion

- [CÓDIGO] Local ledger after hardening: `55` `dod-complete`, `530` pending.
- [CÓDIGO] `brand-xlsx` ledger row points to this review doc and records
  `completed-brand-xlsx-dod`.

## PR Gate Check

- [CÓDIGO] `bash skills/brand-xlsx/scripts/check.sh`: `OK: brand-xlsx artifacts
  validated deterministically`.
- [CÓDIGO] `python3 -B scripts/validate-skill-dod.py --skill brand-xlsx`:
  `skill=brand-xlsx dod=pass errors=0`.
- [CÓDIGO] `python3 -B scripts/validate-skill-scripts.py --strict
  --run-checks --skill brand-xlsx`: `skills_with_scripts=1 warnings=0 errors=0`.
- [CÓDIGO] `python3 -B scripts/validate-skills.py --strict`: `skills=600
  warnings=0 errors=0`.
- [CÓDIGO] `python3 -B scripts/validate-skill-scripts.py --strict
  --run-checks`: `skills_with_scripts=49 warnings=0 errors=0`.
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
- [INFERENCIA] `shellcheck skills/brand-xlsx/scripts/check.sh` was skipped
  because `shellcheck` is not installed in the local environment.

## Release Packet

- [CONFIG] Scope: one active skill, `brand-xlsx`.
- [CONFIG] Branch: `codex/harden-brand-xlsx-dod-20260606`.
- [CÓDIGO] Added deterministic XLSX support through assets, scripts, fixtures,
  eval cases, examples, templates, specialized agents, review doc, and ledger
  update.
- [CONFIG] Decision: open a ready PR only after final gate rerun.

## Decision

[CONFIG] Improved now and ready for PR gate validation.
