# Skill Review: accessibility-testing

Date: 2026-05-28
Reviewer: Codex with three parallel review agents
Status: reviewed and improved
Severity: P2

## Intended Purpose

The skill promises web accessibility testing with axe-core, screen reader testing, keyboard navigation, color contrast validation, and WCAG-oriented evidence.
That means it should produce executable tests, manual scripts, findings, and retest evidence, not generic accessibility advice or unsupported compliance claims.

## Parallel Agent Findings

| Agent | Finding |
|---|---|
| Purpose Auditor | Purpose was aligned, but the skill drifted into remediation and lacked an explicit evidence contract. |
| Artifact Auditor | README, templates, evals, examples, agents, and knowledge files were scaffold-level and did not force accessibility test artifacts. |
| QA/Regression Auditor | Existing evals proved activation only; purpose-specific evals were needed for axe, keyboard, screen reader, contrast, motion, scope, suppressions, and false positives. |

## Current-State Gap

| Area | Gap |
|---|---|
| `SKILL.md` | Mixed testing with remediation, overclaimed WCAG compliance, and did not require pass/fail/not-verified evidence. |
| `knowledge/body-of-knowledge.md` | Placeholder quality metrics instead of accessibility testing concepts, evidence types, and status semantics. |
| `templates/output.md` | Generic summary/evidence/result format rather than an accessibility testing report. |
| `evals/evals.json` | Activation tests, not adversarial accessibility testing behavior. |
| `examples/*` | No realistic route/state/AT testing scenario. |
| `prompts/*` | Generic orchestration, not evidence-first QA execution. |
| `agents/*` | Generic roles, not automation/manual/claim-safety responsibilities. |

## User Impact

A vibe coder could run a quick axe scan, receive a "pass" style report, and believe the app is accessible while dynamic states, keyboard traps, screen reader announcements, contrast, or reduced motion remain untested.
That creates false confidence and can ship regressions to keyboard and assistive-technology users.

## Agent Risk

The agent could convert a clean automated scan into a blanket WCAG claim, hide missing manual coverage, broadly suppress axe findings, or start editing remediation code without explicit user approval.

## Improvement Applied

| File | Change |
|---|---|
| `skills/accessibility-testing/SKILL.md` | Reframed as evidence-first testing/reporting skill, added scope contract, status semantics, manual matrices, suppression governance, and remediation boundary. |
| `skills/accessibility-testing/README.md` | Clarified triggers, required inputs, output contract, non-goals, and no-compliance-claim rule. |
| `skills/accessibility-testing/knowledge/body-of-knowledge.md` | Added evidence model, status model, severity model, test design notes, and quality metrics. |
| `skills/accessibility-testing/templates/output.md` | Replaced generic output with a complete accessibility testing report template. |
| `skills/accessibility-testing/templates/output.docx.md` | Aligned DOCX outline with scope, automated results, manual evidence, findings, suppressions, and limits. |
| `skills/accessibility-testing/templates/output.html` | Added branded report sections for scope, status, automated/manual evidence, findings, and risks. |
| `skills/accessibility-testing/evals/evals.json` | Added purpose-specific evals for stateful axe testing, Jest limits, keyboard scripts, screen reader smoke tests, contrast, reduced motion, scope gaps, suppressions, remediation boundaries, and false positives. |
| `skills/accessibility-testing/examples/*` | Added checkout-flow test input and report-style output with not-verified boundaries. |
| `skills/accessibility-testing/prompts/*` | Aligned quick, deep, primary, and meta prompts to evidence-first accessibility QA. |
| `skills/accessibility-testing/agents/*` | Specialized lead/support/specialist/guardian responsibilities around scope, automation, manual testing, suppressions, and claim safety. |
| `skills/accessibility-testing/knowledge/knowledge-graph.*` | Replaced scaffold graph with accessibility testing concepts and gates. |

## No-Regression Check

Run:

```bash
python3 -m json.tool skills/accessibility-testing/evals/evals.json >/dev/null
python3 -m json.tool skills/accessibility-testing/knowledge/knowledge-graph.json >/dev/null
python3 scripts/validate-skills.py --strict
python3 scripts/qa/run-adversarial-tests.py
jq -e 'length >= 8 and any(.[]; .type=="false_positive") and any(.[]; .id|test("axe|keyboard|screen-reader|contrast|motion|suppression|missing-target"))' skills/accessibility-testing/evals/evals.json
git diff --check
```

Expected:

- Skill validation passes.
- Accessibility testing evals remain valid JSON.
- Targeted eval coverage check returns `true`.
- Ledger reports 524 skills, 4 reviewed, 520 pending after marking this skill reviewed.

## Decision

Improved now.
Next skill in default order: `accessibility-writing`.

## Ledger Completion 2026-06-05

- [CODE] `python3 -B scripts/validate-skill-dod.py --skill accessibility-testing` returned `dod=pass errors=0`.
- [CODE] Added `assets/README.md`, `assets/manifest.json`, and `assets/deliverable-checklist.md` to satisfy the Alfa DoD asset contract.
- [CODE] `skills/accessibility-testing/evals/evals.json` now uses the `cases` contract and includes `assets`, `deterministic_scripts`, and `quality_criteria` in `expected_checks` coverage.
- [CODE] `python3 -B scripts/validate-skills.py --strict` returned `skills=585 warnings=0 errors=0` after this closure batch.
- [CONFIG] Ledger status updated to `dod-complete` with decision `completed-assets-dod`.
