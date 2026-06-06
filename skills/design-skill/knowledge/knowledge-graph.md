# Design Skill — Knowledge Graph

## Core Concepts

- `design-skill`: creates reviewable SKILL.md design specs.
- `frontmatter-policy`: required and supported metadata fields.
- `body-policy`: procedure, quality, anti-pattern, and edge-case constraints.
- `tool-policy`: least-privilege tool profile.
- `moat-score`: completeness, accuracy, actionability, and maintainability score.
- `skill-design-spec`: JSON report validated offline.
- `offline-validator`: validates fixtures without writing final skills.

## Relationships

- `design-skill` produces `skill-design-spec`.
- `frontmatter-policy` constrains `skill-design-spec`.
- `body-policy` validates procedure and sections.
- `tool-policy` validates allowed tools.
- `moat-score` gates readiness.
- `offline-validator` validates `skill-design-spec`.
