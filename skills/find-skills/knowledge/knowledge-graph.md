# Find Skills — Knowledge Graph

## Core Concepts

- `find-skills`: capability discovery and recommendation skill.
- `source-policy`: local-first and remote snapshot rules.
- `candidate`: local, remote, or user-provided skill option.
- `scoring-rubric`: deterministic score and quality tier.
- `install-policy`: confirmation gate and auto-install blocker.
- `recommendation-report`: bounded evidence-tagged output.
- `offline-validator`: script that validates report fixtures without network access.

## Relationships

- `find-skills` reads `source-policy`.
- `source-policy` constrains `candidate`.
- `scoring-rubric` ranks `candidate`.
- `install-policy` guards `recommendation-report`.
- `offline-validator` validates `recommendation-report`.
