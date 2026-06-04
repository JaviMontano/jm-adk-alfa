---
name: x-ray-skill-meta
type: meta
version: 2.0.0
description: "Route requests into X-Ray skill diagnostics."
---

# X-Ray Skill -- Meta Prompt

Activate when the request asks to audit, score, diagnose, x-ray, certify-readiness-check, or review the quality of a skill directory.

## Routing Checks

1. Require a skill path or ask for one.
2. Avoid activation for generic content review unless the artifact is a skill.
3. Prefer quick mode for routing checks and deep mode for release decisions.
