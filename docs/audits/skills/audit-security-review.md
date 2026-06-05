# Skill Review: audit-security

Date: 2026-06-05
Reviewer: Codex multiagent hardening pass
Status: reviewed and improved
Severity: P1

## Intended Purpose

`audit-security` performs a deterministic read-only static security audit of
plugin artifacts across six categories: secret exposure, path security, hook
injection, sensitive files, script safety, and external network risks. [CÓDIGO]
The hardened skill blocks false confidence by requiring exact evidence,
placeholder handling, remediation coverage, category coverage, and validator
checks.

## Spoke Reports

| Spoke | Status | Findings | Coverage Gaps | Recommended Changes | Risk |
|---|---|---|---|---|---|
| Coordinator | complete | [CONFIG] `audit-security` selected as the second skill in the sprint-to-50 batch after `audit-content-quality`; branch created from `origin/main`. | [CONFIG] None. | [CONFIG] Keep branch and PR scoped to one skill. | [CONFIG] Low if scope stays isolated. |
| Determinism Auditor | complete | [CÓDIGO] Pre-hardening skill had read-only/tool drift, no machine-checkable schema, incomplete taxonomy rules, aspirational false-positive policy, scaffold prompts/templates/knowledge, and coarse severity policy. | [CÓDIGO] No assets, scripts, fixtures, deterministic schema, redaction/placeholder policy, or exact category coverage checks existed. | [CONFIG] Add assets, offline validator, fixtures, read-only agents, offline templates, normalized severity policy, and explicit activation/refusal routing. | [INFERENCIA] Medium-high before hardening because security reports could be plausible but non-reproducible. |
| Eval Designer | complete | [CÓDIGO] Evals were activation-only and did not exercise secret exposure, path traversal, absolute paths, hook injection, sensitive files, unsafe downloads, clean plugins, or false positives. | [CÓDIGO] Missing expected checks for exact file, line, pattern, severity, remediation, category coverage, and no file modification. | [CONFIG] Replace evals with 11 deterministic `cases` and suite-level assertions for categories, severities, finding IDs, and forbidden outputs. | [INFERENCIA] High before hardening because core security findings were not tested. |
| Guardian | complete | [CÓDIGO] Initial DoD failed for missing `assets/`, scaffold examples, evals without `cases`, absent review doc, pending ledger, mutable agent tools, and missing prompt sections. | [CÓDIGO] Ledger completion required assets, deterministic scripts, eval cases, examples, review evidence, and passing validations. | [CONFIG] Block ledger closure until per-skill DoD and script gates pass. | [INFERENCIA] Low after local validation, pending full PR gates. |

## Hardening Brief

- [CONFIG] Add deterministic assets for activation routing, scan policy, report
  contract, evidence policy, and asset manifest.
- [CONFIG] Add `scripts/validate_security_report.py`, `scripts/check.sh`, one
  valid fixture, and two negative fixtures for placeholder severity and missing
  category coverage.
- [CONFIG] Replace scaffold README, examples, evals, agents, prompts, templates,
  knowledge files, and pattern reference with security-specific contracts.
- [CONFIG] Normalize the scan taxonomy to six categories and define severity,
  status, placeholder, remediation, and coverage rules.
- [CONFIG] Remove mutation tools from agents and remove remote assets from
  templates.

## Improvement Applied

| Area | Change |
|---|---|
| `SKILL.md` | [CÓDIGO] Added deterministic assets, activation/refusal routing, six-category taxonomy, severity policy, output contract, validator command, and read-only limits. |
| `README.md` | [CÓDIGO] Replaced scaffold text with local resources, checks, and decision rule. |
| `assets/` | [CÓDIGO] Added activation policy, scan policy, report contract, evidence policy, manifest, and README. |
| `scripts/` | [CÓDIGO] Added offline report validator, check script, valid fixture, placeholder-critical negative fixture, and missing-category negative fixture. |
| `evals/evals.json` | [CÓDIGO] Replaced root-array evals with 11 `cases` covering real secrets, placeholders, traversal, hardcoded paths, hook injection, sensitive files, unsafe downloads, clean plugin, false positives, missing targets, and exploit refusal. |
| `examples/*` | [CÓDIGO] Added realistic input and output with seven findings and all six categories. |
| `agents/*` and `prompts/*` | [CÓDIGO] Specialized read-only roles and prompts around static scan coverage, evidence, remediation, and refusal routing. |
| `templates/*` | [CÓDIGO] Replaced scaffold and remote-font templates with offline Markdown, HTML, and DOCX-oriented report templates. |
| `knowledge/*` and `references/security-patterns.md` | [CÓDIGO] Added normalized category taxonomy, evidence tags, invariants, anti-patterns, and a security-specific knowledge graph. |

## Per-Skill No-Regression Check

Observed on 2026-06-05:

```bash
bash skills/audit-security/scripts/check.sh
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill audit-security
python3 -B scripts/validate-skill-dod.py --skill audit-security
python3 -B scripts/validate-skills.py --strict
```

Results:

- [CÓDIGO] `OK: audit-security reports validated deterministically`
- [CÓDIGO] `skills_with_scripts=1 warnings=0 errors=0`
- [CÓDIGO] `skill=audit-security dod=pass errors=0`
- [CÓDIGO] `skills=600 warnings=0 errors=0`

## Follow-Up Gap

- [INFERENCIA] The validator proves report structure, category coverage,
  severity counts, stable finding IDs, placeholder handling, and remediation
  coverage; it does not prove absence of obfuscated, encrypted, or split
  secrets outside the static patterns.

## Decision

[CONFIG] Improved now and ready for full PR validation.

## Ledger Completion 2026-06-05

- [CÓDIGO] `bash skills/audit-security/scripts/check.sh` passed with valid,
  invalid placeholder-critical, and invalid missing-category fixtures.
- [CÓDIGO] `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill audit-security` passed with `warnings=0 errors=0`.
- [CÓDIGO] `python3 -B scripts/validate-skill-dod.py --skill audit-security` passed with `dod=pass errors=0`.

## PR Gate Check 2026-06-05

- [CÓDIGO] `python3 -B scripts/validate-skills.py --strict` passed with
  `skills=600 warnings=0 errors=0`.
- [CÓDIGO] `python3 -B scripts/validate-skill-scripts.py --strict --run-checks`
  passed with `skills_with_scripts=44 warnings=0 errors=0`.
- [CÓDIGO] `python3 -B scripts/count-components.py --check-docs` passed with
  `skills=600 agents=261 commands=267 prompts=256 components=1384`.
- [CÓDIGO] `bash scripts/check-repo-boundaries.sh` passed with
  `Repo boundaries OK`.
- [CÓDIGO] `python3 -B scripts/validate-runtime-instructions.py` passed.
- [CÓDIGO] `python3 -B scripts/qa/run-adversarial-tests.py` passed with
  `passed=11 failed=0 total=11`.
- [CÓDIGO] `python3 -B scripts/qa/run-confidence-fp-tests.py` passed.
- [CÓDIGO] `python3 -B scripts/post_annotations.py --validate-only references/schemas/annotations.example.json`
  passed with `valid annotations`.
- [CÓDIGO] `bash scripts/doc-factory/check.sh` passed.
- [CÓDIGO] `python3 -B scripts/diagnose-user-context.py --dry-run` reported
  `ready`.
- [CÓDIGO] `python3 -B scripts/diagnose-personal-skills.py --dry-run`
  completed with no personal skills to diagnose.
- [CÓDIGO] `python3 -B scripts/sync-personal-skills.py --dry-run --target /tmp/alfa-personal-skills-target`
  completed with `files=0`.
- [CÓDIGO] `bash scripts/adapt.sh all` regenerated adapters for `600` skills.
- [CÓDIGO] `bash scripts/generate-pristino-index.sh` regenerated
  `PRISTINO-INDEX.md` with `Agents: 261 | Skills: 600 | Commands: 267 |
  Prompts: 256 | Components: 1384`.
- [CÓDIGO] `git diff --check` passed with no whitespace findings.
- [CÓDIGO] `shellcheck skills/audit-security/scripts/check.sh` was skipped
  because `shellcheck` is not installed in the local environment.
