---
name: admin-dashboards-meta
type: self-improvement
version: 2.0.0
description: "Evaluate and improve the Admin Dashboards skill."
---

# Admin Dashboards — Self-Improvement

## Evaluate

1. Does `knowledge/body-of-knowledge.md` still cover data contracts, RBAC, tables, CRUD, metrics, realtime, exports, audit, states, accessibility, responsive, and performance?
2. Are the 4 sub-agents blocking invented APIs, hidden-only RBAC, unsafe exports, and happy-path CRUD?
3. Are templates producing implementation-ready dashboard specs rather than generic summaries?
4. Do evals catch large datasets, missing backend evidence, permission deeplinks, injection/export issues, and no-write analysis mode?
5. Have real projects introduced new table libraries, chart libraries, auth patterns, or audit requirements?
6. Has the related skill landscape changed: `api-design`, `api-security`, `audit-trail-design`, `form-engineering`, `accessibility-testing`, `data-visualization`?

## Improve

1. Update contracts and gates based on field failures.
2. Add evals for any discovered false pass or unsafe admin workflow.
3. Refine quality criteria when implementation bugs reveal missing states.
4. Update knowledge graph with new contracts, gates, and related skills.
5. Test templates with adversarial dashboard inputs before accepting changes.
6. Escalate broader guardrails only when ambiguity repeats across skills.

## Trigger

Run this meta-prompt when:
- Skill hasn't been reviewed in 30+ days
- User reports unexpected output quality
- New related skills added to the kit
- Insights file updated with relevant patterns
