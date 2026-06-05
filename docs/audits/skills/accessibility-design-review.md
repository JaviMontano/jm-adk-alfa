# Skill Review: accessibility-design

Date: 2026-05-28
Reviewer: Codex with three parallel review agents
Status: reviewed and improved
Severity: P2

## Intended Purpose

The skill promises WCAG 2.1 AA accessibility patterns for web applications:
ARIA roles, keyboard navigation, screen reader support, color contrast, and inclusive design.
That means it should produce accessible design and implementation specifications, not an audit report.

## Parallel Agent Findings

| Agent | Finding |
|---|---|
| Purpose Auditor | The headline purpose is strong, but the implementation contract was generic and drifted toward audit/testing. |
| Artifact Auditor | README, templates, evals, examples, agents, and knowledge were scaffold-level and did not force a design deliverable. |
| Regression Auditor | Existing evals only proved activation; purpose-specific evals were needed for ARIA overuse, keyboard maps, contrast tokens, forms, focus, motion, and false positives. |

## Current-State Gap

| Area | Gap |
|---|---|
| `SKILL.md` | No explicit design-vs-audit boundary; incomplete component-pattern and acceptance-criteria contract. |
| `knowledge/body-of-knowledge.md` | Placeholder standards language instead of accessible design principles and component pattern requirements. |
| `templates/output.md` | Generic summary/evidence/result format rather than an accessible interaction spec. |
| `evals/evals.json` | Activation tests, not accessible design behavior tests. |
| `examples/*` | No realistic component spec output. |
| `prompts/*` | Generic orchestration, not accessible design spec production. |
| `agents/*` | Generic roles, not component/WCAG/ARIA/focus/token responsibilities. |

## User Impact

A vibe coder could ask for accessible design and receive broad advice without keyboard maps, focus rules, ARIA decisions, token requirements, or acceptance criteria.
That creates implementation drift and leaves accessibility to late-stage QA.

## Agent Risk

The agent could overuse ARIA, omit focus return, overclaim contrast without ratios, skip reduced-motion requirements, or route audit requests into a design skill.

## Improvement Applied

| File | Change |
|---|---|
| `skills/accessibility-design/SKILL.md` | Reframed as accessible design/implementation skill, added boundary with audit/testing, component behavior, keyboard/focus, content, tokens, and acceptance criteria. |
| `skills/accessibility-design/README.md` | Clarified scope, triggers, output shape, and non-goals. |
| `skills/accessibility-design/knowledge/body-of-knowledge.md` | Added POUR mapping, component pattern checklist, token requirements, output contract, and quality metrics. |
| `skills/accessibility-design/templates/output.md` | Replaced generic output with accessible interaction spec template. |
| `skills/accessibility-design/evals/evals.json` | Added purpose-specific evals for modal, tabs, ARIA overuse, contrast token gaps, form errors, reduced motion, and false positives. |
| `skills/accessibility-design/examples/*` | Added realistic coupon modal input and expected accessible design output. |
| `skills/accessibility-design/prompts/*` | Aligned execution to accessible design spec and not-verified boundaries. |
| `skills/accessibility-design/agents/*` | Specialized lead/support/specialist/guardian responsibilities. |

## No-Regression Check

Run:

```bash
python3 -m json.tool skills/accessibility-design/evals/evals.json >/dev/null
python3 -m json.tool skills/accessibility-design/knowledge/knowledge-graph.json >/dev/null
python3 scripts/validate-skills.py --strict
python3 scripts/qa/run-adversarial-tests.py
jq -e 'length >= 8 and any(.[]; .type=="false_positive") and any(.[]; .id|test("aria|keyboard|contrast|focus|form|motion|modal|tabs"))' skills/accessibility-design/evals/evals.json
git diff --check
```

Expected:

- Skill validation passes.
- Accessibility design evals remain valid JSON.
- Targeted eval coverage check returns `true`.
- Ledger reports 524 skills, 3 reviewed, 521 pending after marking this skill reviewed.

## Decision

Improved now.
Next skill in default order: `accessibility-testing`.

## Ledger Completion 2026-06-05

- [CODE] `python3 -B scripts/validate-skill-dod.py --skill accessibility-design` returned `dod=pass errors=0`.
- [CODE] Added `assets/README.md`, `assets/manifest.json`, and `assets/deliverable-checklist.md` to satisfy the Alfa DoD asset contract.
- [CODE] `skills/accessibility-design/evals/evals.json` now uses the `cases` contract and includes `assets`, `deterministic_scripts`, and `quality_criteria` in `expected_checks` coverage.
- [CODE] `python3 -B scripts/validate-skills.py --strict` returned `skills=585 warnings=0 errors=0` after this closure batch.
- [CONFIG] Ledger status updated to `dod-complete` with decision `completed-assets-dod`.
