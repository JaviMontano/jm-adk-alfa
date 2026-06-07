# AI CONOPS - Body of Knowledge

## Canon
AI CONOPS defines the operational concept before architecture: system purpose,
stakeholders, autonomy level, value rationale, success metrics, operating modes,
assumptions, and risks.

## Core Decisions
| Decision | Deterministic Requirement |
|----------|---------------------------|
| system vision | problem statement, objectives, success criteria |
| stakeholders | at least three roles with concerns and decision rights |
| interaction level | exactly one Level 1-5 default with rationale |
| business value | value score, effort score, and matching quadrant |
| metrics | technical, business, and UX/ethics pillars covered |
| operational modes | Startup, Executing, Degraded, and Recovery included |
| assumptions | explicit ids, owners, and status |

## Reference Policy
- Use `references/interaction-spectrum.md` for autonomy level selection.
- Use `references/business-value-matrix.md` for quadrant classification.
- Use `references/success-metrics.md` for metric pillars and stakeholder alignment.

## Quality Metrics
| Metric | Target | How to Measure |
|--------|--------|---------------|
| Stakeholder coverage | >= 3 stakeholders | Validator stakeholder count |
| Metric pillar coverage | 3/3 pillars | Validator pillar set |
| Mode coverage | Required modes present | Validator mode set |
| Assumption transparency | 100% explicit | Assumption list with owners |
| Validation gate pass | 100% | `scripts/check.sh` and DoD validators |

## Anti-Patterns
- Starting with model or architecture selection before operational concept.
- Hiding assumptions inside narrative prose.
- Calling a high-effort low-value initiative a Quick Win.
- Choosing high autonomy without controls, auditability, and rollback.
- Measuring only model accuracy while ignoring business and UX/ethics outcomes.
