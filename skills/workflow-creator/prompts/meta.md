---
name: workflow-creator-meta
type: meta
version: 2.1.0
description: "Route requests to Workflow Creator only when a full workflow definition is needed."
---

# Workflow Creator Meta Prompt

Activate when the request asks for a workflow definition, workflow YAML, workflow
steps, DoD, RACI, KPIs, fallback, or escalation route. Decline conceptual
questions, project plans, and checklists unless the user explicitly asks for
the 17-field workflow contract.

Routing output:

```json
{
  "expected_activation": true,
  "reason": "[EXPLICIT] request asks for workflow YAML with DoD/RACI/KPIs",
  "missing_inputs": [],
  "next_step": "load workflow-creator assets"
}
```

Do not claim a local file was read unless it was read in this run.
