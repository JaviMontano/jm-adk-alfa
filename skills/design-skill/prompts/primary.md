---
name: design-skill-primary
type: execution
version: 2.0.0
description: "Execute the Design Skill workflow."
triad:
  lead: "design-skill-lead"
  support: "design-skill-support"
  guardian: "design-skill-guardian"
---

# Design Skill — Execute

1. Parse skill slug, concept, movement, owning agent, depth, and tool needs.
2. Load `assets/frontmatter-policy.json`, `assets/body-policy.json`, `assets/tool-policy.json`, and `assets/report-contract.json`.
3. Draft frontmatter, guiding principle, procedure, quality criteria, anti-patterns, edge cases, tool rationale, and MOAT score.
4. Enforce least-privilege tools and block invalid name, vague procedure, weak criteria, missing edge cases, and MOAT score below 75.
5. Validate JSON specs with `scripts/validate_design_skill_spec.py` when a spec artifact is produced.
