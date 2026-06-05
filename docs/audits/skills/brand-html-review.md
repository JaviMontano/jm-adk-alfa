# Skill Review: brand-html

Date: 2026-06-05
Reviewer: Codex multiagent hardening pass
Status: reviewed and improved
Severity: P1

## Intended Purpose

`brand-html` generates deterministic, brand-token-compliant single-file HTML
artifacts from a supplied brand configuration or explicit fallback defaults.
[CÓDIGO] It enforces CSS variables, semantic structure, responsive CSS,
SVG favicon links, accessibility, dependency boundaries, and offline validation
fixtures. [CONFIG]

## Spoke Reports

| Spoke | Status | Findings | Coverage Gaps | Recommended Changes | Risk |
|---|---|---|---|---|---|
| Coordinator | complete | [CONFIG] `brand-html` selected after `code-review-checklist`; branch created from `origin/main`. | [CONFIG] None. | [CONFIG] Keep branch and PR scoped to one skill. | [CONFIG] Low if scope remains isolated. |
| Determinism Auditor | complete | [CÓDIGO] DoD failed before hardening: missing assets, scaffold README/examples/knowledge, list-style evals, remote fonts, implicit date placeholders, token drift, tool drift, and no validator. | [CÓDIGO] Missing output contract, fallback config, evidence policy, fixtures, scripts, review doc, and ledger closure. | [CONFIG] Add deterministic assets/scripts, replace scaffold content, constrain dependencies/time, align tools, and close ledger only after validation. | [INFERENCIA] High before hardening because generated HTML could violate token, dependency, or evidence rules. |
| Eval Designer | complete | [CÓDIGO] Evals covered only activation, dark hero, no config, RTL, and DOCX false positive as prose. | [CÓDIGO] Missing deterministic checks for structure, CSS variables, SVG favicon, contrast, remote dependencies, responsive CSS, invalid fixtures, and token-only false positives. | [CONFIG] Add 13 `cases` plus validator fixtures for valid landing, RTL, off-token color, low contrast, external dependency rejection, and non-SVG favicon rejection. | [INFERENCIA] Medium-high before hardening because visual output could look acceptable while failing contract. |
| Guardian | complete | [CÓDIGO] Initial `validate-skill-dod.py --skill brand-html` failed with 5 errors and ledger remained pending. | [CÓDIGO] Assets, eval cases, examples, review doc, and ledger evidence were absent. | [CONFIG] Block closure until DoD and script checks pass. | [INFERENCIA] Closure-blocking until local validation passes. |

## Hardening Brief

- [CONFIG] Add activation, HTML contract, SVG favicon, fallback config,
  evidence, and manifest assets.
- [CONFIG] Add `scripts/validate_brand_html.py`, `scripts/check.sh`, two valid
  fixtures, and four negative fixtures.
- [CONFIG] Replace scaffold README, examples, evals, agents, prompts, templates,
  knowledge, and reference content.
- [CONFIG] Remove `Edit`, constrain `Write` to requested artifact generation,
  and keep validation deterministic.
- [CONFIG] Update ledger only after per-skill validators pass.

## Improvement Applied

| Area | Change |
|---|---|
| `SKILL.md` | [CÓDIGO] Added activation routing, deterministic resources, token rules, single-file output contract, accessibility/layout gates, dependency boundaries, and validation commands. |
| `README.md` | [CÓDIGO] Replaced scaffold text with triggers, assets, scripts, and output contract. |
| `assets/` | [CÓDIGO] Added activation policy, HTML contract, SVG favicon policy, fallback favicon asset, fallback config, evidence policy, manifest, and README. |
| `scripts/` | [CÓDIGO] Added offline HTML validator, check script, valid landing/RTL fixtures, and invalid hardcoded-color, low-contrast, external-dependency, and non-SVG favicon fixtures. |
| `evals/evals.json` | [CÓDIGO] Replaced root-array evals with 13 `cases` covering tokenized output, SVG favicon, dark hero, fallback, font fallback, RTL, dark mode, negative fixtures, false positives, and adversarial validation. |
| `examples/*` | [CÓDIGO] Added realistic brand-token input and single-file HTML output with validation evidence. |
| `agents/*` and `prompts/*` | [CÓDIGO] Specialized roles around HTML generation, token compliance, false-positive routing, and guardian blocking. |
| `templates/*` | [CÓDIGO] Replaced scaffold and remote-font templates with tokenized offline HTML/Markdown/DOCX handoff templates. |
| `knowledge/*` and `references/domain-knowledge.md` | [CÓDIGO] Added deterministic HTML invariants, false positives, validation rules, and anti-patterns. |

## Follow-Up Gap

- [INFERENCIA] The validator proves static HTML contract features, but rendered
  visual quality still requires browser inspection when a user asks for
  pixel-level fidelity.

## Ledger Completion

- [CÓDIGO] Local ledger after hardening: `53` `dod-complete`, `532` pending.
- [CÓDIGO] `brand-html` ledger row points to this review doc and records
  `completed-assets-dod`.

## PR Gate Check

- [CÓDIGO] `bash skills/brand-html/scripts/check.sh`: `OK: brand-html artifacts
  validated deterministically`.
- [CÓDIGO] `python3 -B scripts/validate-skill-dod.py --skill brand-html`:
  `skill=brand-html dod=pass errors=0`.
- [CÓDIGO] `python3 -B scripts/validate-skill-scripts.py --strict
  --run-checks --skill brand-html`: `skills_with_scripts=1 warnings=0 errors=0`.
- [CÓDIGO] `python3 -B scripts/validate-skills.py --strict`: `skills=600
  warnings=0 errors=0`.
- [CÓDIGO] `python3 -B scripts/validate-skill-scripts.py --strict
  --run-checks`: `skills_with_scripts=47 warnings=0 errors=0`.
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
- [INFERENCIA] `shellcheck skills/brand-html/scripts/check.sh` was skipped
  because `shellcheck` is not installed in the local environment.

## Release Packet

- [CONFIG] Scope: one active skill, `brand-html`.
- [CONFIG] Branch: `codex/harden-brand-html-dod-20260605`.
- [CÓDIGO] Added deterministic SVG favicon support through
  `assets/favicon.svg`, `assets/favicon-policy.json`, HTML template link,
  validator checks, and valid/negative fixtures.
- [CONFIG] Decision: open a ready PR after final rerun of key gates.

## Decision

[CONFIG] Improved now and ready for PR delivery.
