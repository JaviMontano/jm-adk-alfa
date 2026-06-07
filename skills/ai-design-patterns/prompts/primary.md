---
name: ai-design-patterns-primary
type: execution
version: 2.1.0
description: "Execute deterministic AI pattern selection with evidence and dependency checks."
triad:
  lead: "ai-design-patterns-lead"
  support: "ai-design-patterns-support"
  guardian: "ai-design-patterns-guardian"
---

# AI Design Patterns - Execute

## Execution
1. Load `references/ai-patterns-detail.md`, `references/tactics-catalog.md`, and `references/anti-patterns.md`.
2. Load assets under `assets/`.
3. Establish requirements, constraints, risk level, model count, traffic profile, and detected context.
4. Detect anti-patterns with evidence.
5. Recommend patterns with priority, rationale, trade-offs, tactics, dependencies, and evidence.
6. Build roadmap phases with exit criteria.
7. Guardian validates JSON packets with `scripts/validate_ai_design_patterns_report.py`.

## Output
- Requirements and detected context.
- Anti-pattern detection.
- Pattern recommendations.
- Tactic mapping.
- Dependency checks.
- Implementation roadmap and risks.
