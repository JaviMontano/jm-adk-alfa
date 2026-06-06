---
name: design-agent-primary
type: execution
version: 2.0.0
description: "Execute the Design Agent workflow."
triad:
  lead: "design-agent-lead"
  support: "design-agent-support"
  guardian: "design-agent-guardian"
---

# Design Agent — Execute

1. Parse agent name, plugin context, handled commands, skills, tools, and interaction points.
2. Load `assets/frontmatter-policy.json`, `assets/constraint-policy.json`, `assets/maxturns-policy.json`, and `assets/report-contract.json`.
3. Draft frontmatter with required fields and no forbidden plugin subagent fields.
4. Define role boundary, skill assignments, command flows, operating principles, and maxTurns rationale.
5. Validate tools/disallowedTools exclusivity and command flow coverage.
6. Validate JSON specs with `scripts/validate_design_agent_spec.py` when a spec artifact is produced.
