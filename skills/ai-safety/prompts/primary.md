---
name: ai-safety-primary
type: execution
version: 2.1.0
description: "Execute deterministic AI safety report generation."
triad:
  lead: "ai-safety-lead"
  support: "ai-safety-support"
  guardian: "ai-safety-guardian"
---

# AI Safety - Execute

1. Load `SKILL.md` and `assets/*.json`.
2. Build evidence ids.
3. Classify risks with severity and scenarios.
4. Map every risk to controls.
5. Add jailbreak tests, evaluation metrics, and escalation.
6. Validate the report offline before delivery.
