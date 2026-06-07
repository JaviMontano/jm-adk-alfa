---
name: alerting-strategy-primary
type: execution
version: 2.1.0
description: "Execute deterministic Alerting Strategy workflow."
triad:
  lead: "alerting-strategy-lead"
  support: "alerting-strategy-support"
  guardian: "alerting-strategy-guardian"
---

# Alerting Strategy - Execute

1. Confirm the request concerns alert severity, routing, escalation, paging, thresholds, or alert fatigue.
2. Read `assets/manifest.json` and contract assets.
3. Gather evidence: incident history, metric names, owners, response targets, and constraints.
4. Produce severity model, alert rules, escalation paths, fatigue controls, routing policy, validation checks, and risks.
5. If JSON handoff exists, validate it with `scripts/validate_alerting_strategy.py`.
