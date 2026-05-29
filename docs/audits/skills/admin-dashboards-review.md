# Skill Review: admin-dashboards

Date: 2026-05-28
Reviewer: Codex with three parallel review agents
Status: reviewed and improved
Severity: P1

## Intended Purpose

The skill promises admin dashboards with data tables, filters, charts, CRUD operations, realtime updates, layout patterns, and state management.
For a developer kit, that must become an implementation-ready contract for data, permissions, states, security, auditability, responsive behavior, and tests.

## Parallel Agent Findings

| Agent | Finding |
|---|---|
| Purpose Auditor | RBAC and security were promised but not operationalized into UI/API enforcement, negative tests, or audit requirements. |
| Artifact Auditor | README, evals, examples, templates, agents, and knowledge files were scaffold-level and did not force a dashboard spec. |
| QA/Regression Auditor | Evals needed adversarial coverage for invented APIs, large tables, CRUD failures, RBAC deeplinks, injection/export risks, empty/error states, KPI integrity, audit trails, responsive/a11y, realtime fallback, and no-write analysis mode. |

## Current-State Gap

| Area | Gap |
|---|---|
| `SKILL.md` | Good feature list, but no hard contracts for backend evidence, RBAC matrix, states, exports, audit, or metric integrity. |
| `README.md` | Scaffold text and weak discoverability. |
| `knowledge/body-of-knowledge.md` | Generic standards language instead of dashboard operating contracts. |
| `templates/output.md` | Generic summary/evidence/result output rather than admin dashboard spec. |
| `evals/evals.json` | Activation tests, not behavior or safety tests. |
| `examples/*` | Placeholder input/output without realistic CRM/dashboard scenario. |
| `prompts/*` | Generic orchestration and inflated confidence target. |
| `agents/*` | Generic responsibilities that did not block unsafe admin workflows. |
| `knowledge/knowledge-graph.*` | Placeholder concepts instead of contracts and gates. |

## User Impact

A vibe coder could generate a visually plausible admin panel that hides buttons but lacks backend authorization, invents APIs or KPIs, exports sensitive data, fails on empty/error states, or breaks on large datasets.

## Agent Risk

The agent could overbuild UI before data and permission contracts exist, assume Firestore/WebSocket/API routes without evidence, claim performance without measurement, or mutate files when the user asked only for a spec.

## Improvement Applied

| File | Change |
|---|---|
| `skills/admin-dashboards/SKILL.md` | Added data contract, RBAC/backend enforcement, state matrix, audit/export, security, responsive, accessibility, and no-invented-backend gates. |
| `skills/admin-dashboards/README.md` | Added natural triggers, minimum inputs, output contract, and not-verified rule. |
| `skills/admin-dashboards/knowledge/body-of-knowledge.md` | Added core contracts, quality metrics, and operational design rules. |
| `skills/admin-dashboards/templates/output.md` | Replaced generic output with implementation-ready dashboard spec sections. |
| `skills/admin-dashboards/templates/output.docx.md` | Aligned DOCX outline with dashboard contracts and gates. |
| `skills/admin-dashboards/templates/output.html` | Added HTML sections for scope, data, RBAC, tables, CRUD, metrics, states, gates, and tests. |
| `skills/admin-dashboards/evals/evals.json` | Added 12 purpose-specific evals for API no-invention, server-side tables, CRUD failures, RBAC deeplinks, security/export, states, KPI integrity, audit, responsive/a11y, realtime fallback, no-write mode, and false positives. |
| `skills/admin-dashboards/examples/*` | Added realistic CRM input and spec-style output. |
| `skills/admin-dashboards/prompts/*` | Aligned prompt variants to evidence-first dashboard contracts and BMAD readiness. |
| `skills/admin-dashboards/agents/*` | Specialized lead/support/specialist/guardian responsibilities around data, RBAC, tables, CRUD, audit, export, performance, and accessibility. |
| `skills/admin-dashboards/knowledge/knowledge-graph.*` | Replaced scaffold graph with admin-dashboard contracts and gates. |

## No-Regression Check

Run:

```bash
python3 -m json.tool skills/admin-dashboards/evals/evals.json >/dev/null
python3 -m json.tool skills/admin-dashboards/knowledge/knowledge-graph.json >/dev/null
python3 scripts/validate-skills.py --strict
python3 scripts/qa/run-adversarial-tests.py
jq -e 'length >= 10 and any(.[]; .type=="false_positive") and all(.[]; has("id") and has("type") and has("input") and has("expected_behavior") and has("must_include") and has("must_not_include") and has("tags"))' skills/admin-dashboards/evals/evals.json
jq -e '(["data-contract","RBAC","table","CRUD","metrics","realtime","export","states","security","accessibility","responsive","audit","false_positive"] - ([.[] | (.tags[]?, .type)] | unique) | length) == 0' skills/admin-dashboards/evals/evals.json
rg -n 'generated-by|Example output|realistic project request|Industry standards for this domain|Best practice guides|Related skills in this domain|Produces the primary deliverable|Deep expertise in advanced patterns|Markdown with summary|\{summary\}|\{evidence\}|\{result\}|\{validation\}|\{risks\}|Confidence >= 0.95' skills/admin-dashboards
git diff --check
```

Expected:

- Skill validation passes.
- Admin dashboard evals remain valid JSON.
- Targeted eval coverage checks return `true`.
- Scaffold-debt `rg` returns no matches.
- Ledger reports 524 skills, 7 reviewed, 517 pending after marking this skill reviewed.

## Decision

Improved now.
Next skill in default order: `agent-constitution-creator`.
