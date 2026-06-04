# X-Ray Skill -- Knowledge Graph

## Core Concepts

- [[rubric-score]] -- 10 quality dimensions scored from 1 to 10.
- [[validation-gate]] -- 13 binary checkpoints that gate certification readiness.
- [[component-classification]] -- directory and file inventory tagged as strength or gap.
- [[certification-readiness]] -- `CERTIFIED`, `CONDITIONAL`, or `BLOCKED`.
- [[deterministic-compiler]] -- `scripts/compile-x-ray-report.py` read-only report generator.

## Skill Relationships

- Upstream: `skill-creator` and `creator-moat-skill` provide quality standards.
- Downstream: `surgeon-skill` fixes issues and `certify-skill` finalizes readiness.
