# Design Agent — Knowledge Graph

## Core Concepts

- `design-agent`: creates reviewable plugin subagent specs.
- `frontmatter-policy`: supported, required, forbidden, and mutually exclusive fields.
- `constraint-policy`: plugin subagent limitations.
- `maxturns-policy`: deterministic turn budget formula.
- `agent-design-spec`: JSON report validated offline.
- `operating-principle`: specific, actionable, verifiable behavioral rule.
- `offline-validator`: validates fixtures without writing deployable agent files.

## Relationships

- `design-agent` uses `frontmatter-policy`.
- `constraint-policy` blocks forbidden fields.
- `maxturns-policy` validates `maxTurns`.
- `agent-design-spec` contains skills, flows, and principles.
- `offline-validator` validates `agent-design-spec`.
