---
name: workspace-governance-meta
type: self-improvement
version: 2.0.0
description: "Evaluate and improve the Workspace Governance skill."
---

# Workspace Governance — Self-Improvement

## Evaluate

1. Are workspace path, session, task bridge, and gitignore policies current?
2. Do fixtures cover missing `.gitignore`, invalid session names, missing READMEs, stale sessions, and unsafe action targets?
3. Are task bridge patterns still aligned with tasklog IDs?
4. Are estandares expectations documented and discoverable?

## Improve

1. Update assets and fixtures when workspace policy changes.
2. Add eval cases for new stale-session or task bridge edge cases.
3. Refine Guardian path safety if allowed workspace paths change.
4. Keep report validation offline and deterministic.

## Trigger

Run this meta-prompt when:
- Skill hasn't been reviewed in 30+ days
- User reports unexpected output quality
- New related skills added to the kit
- Insights file updated with relevant patterns
