# Skill Review: accessibility-audit

Date: 2026-05-28
Reviewer: Codex with three parallel review agents
Status: reviewed and improved
Severity: P2

## Intended Purpose

The skill promises WCAG 2.1 AA automated scanning with axe-core plus manual checklist coverage for keyboard, screen reader, and contrast.
That means it should produce an evidence-backed digital accessibility audit report, not a generic quality-analysis response.

## Parallel Agent Findings

| Agent | Finding |
|---|---|
| Purpose Auditor | `SKILL.md` aligned at the headline level but treated axe severity as a compliance gate, lacked criterion-level manual coverage, and included an uncited percentage claim. |
| Artifact Auditor | README, templates, evals, examples, prompts, agents, and knowledge were mostly scaffold-level and did not force an audit-ready output. |
| Regression Auditor | Existing validators proved structure only; purpose-specific evals were needed for clean axe/manual failure, missing evidence, skipped screen reader checks, ARIA overuse, and false positives. |

## Current-State Gap

| Area | Gap |
|---|---|
| `SKILL.md` | High-level policy, not an executable audit protocol; no strict separation between automated evidence and manual finality. |
| `knowledge/body-of-knowledge.md` | Placeholder standards language instead of WCAG audit map, status model, severity, and ticket contract. |
| `templates/output.md` | Generic summary/evidence/result format rather than an audit report. |
| `evals/evals.json` | Generic activation cases rather than accessibility failure modes. |
| `examples/*` | No realistic scope, evidence, or final status. |
| `prompts/*` | Referenced stale sections such as `When to Activate` and `Validation Gate`. |
| `agents/*` | Generic role descriptions, not accessibility-specific duties. |

## User Impact

A vibe coder could receive a plausible "accessibility audit" that says automation passed while keyboard, screen reader, contrast, or form behavior remains broken.
The user may then ship inaccessible UI with false confidence.

## Agent Risk

The agent could overclaim WCAG compliance, skip manual evidence, hide not-verified areas, add unnecessary ARIA, or produce findings that are not actionable by an owner.

## Improvement Applied

| File | Change |
|---|---|
| `skills/accessibility-audit/SKILL.md` | Rewrote purpose, laws, protocol, remediation rules, quality gates, edge cases, and limits around evidence-backed WCAG audit finality. |
| `skills/accessibility-audit/README.md` | Clarified triggers, tools, default audit output, and remediation boundary. |
| `skills/accessibility-audit/knowledge/body-of-knowledge.md` | Added WCAG audit map, status model, severity model, remediation ticket contract, and quality metrics. |
| `skills/accessibility-audit/templates/output.md` | Replaced generic output with structured audit report template. |
| `skills/accessibility-audit/evals/evals.json` | Added purpose-specific happy path, clean-axe/manual-fail, missing-evidence, violation bundle, skipped screen reader, ARIA overuse, and false-positive cases. |
| `skills/accessibility-audit/examples/*` | Added realistic checkout-flow audit input and fail-status output. |
| `skills/accessibility-audit/prompts/*` | Updated routing/execution to use actual `Purpose`, `Protocol`, and `Quality Gates` sections. |
| `skills/accessibility-audit/agents/*` | Made lead/support/specialist/guardian responsibilities accessibility-specific. |

## No-Regression Check

Run:

```bash
python3 -m json.tool skills/accessibility-audit/evals/evals.json >/dev/null
python3 -m json.tool skills/accessibility-audit/knowledge/knowledge-graph.json >/dev/null
python3 scripts/validate-skills.py --strict
python3 scripts/qa/run-adversarial-tests.py
git diff --check
```

Expected:

- Skill validation passes.
- Accessibility audit evals remain valid JSON.
- No stale `When to Activate`, `Validation Gate`, or uncited percentage claims remain.
- Ledger reports 524 skills, 2 reviewed, 522 pending after marking this skill reviewed.

## Decision

Improved now.
Next skill in default order: `accessibility-design`.

## Ledger Completion 2026-06-05

- [CODE] `python3 -B scripts/validate-skill-dod.py --skill accessibility-audit` returned `dod=pass errors=0`.
- [CODE] Added `assets/README.md`, `assets/manifest.json`, and `assets/deliverable-checklist.md` to satisfy the Alfa DoD asset contract.
- [CODE] `skills/accessibility-audit/evals/evals.json` now uses the `cases` contract and includes `assets`, `deterministic_scripts`, and `quality_criteria` in `expected_checks` coverage.
- [CODE] `python3 -B scripts/validate-skills.py --strict` returned `skills=585 warnings=0 errors=0` after this closure batch.
- [CONFIG] Ledger status updated to `dod-complete` with decision `completed-assets-dod`.
