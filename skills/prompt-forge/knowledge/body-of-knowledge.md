# Prompt Forge - Body Of Knowledge

## Canon

Prompt Forge is a deterministic prompt artifact workflow. It converts a user goal or existing prompt into one of five outputs: create, review, evolve, repair, or port.

## Core Concepts

| Concept | Definition | Gate |
|---|---|---|
| Playbook | Canonical system prompt structure with required sections. | Must match `assets/playbook-contract.json`. |
| Source boundary | Explicit list of allowed evidence and unsupported-source behavior. | Must prevent invented facts. |
| Rubric scorecard | Ten named criteria scored with evidence and repairs. | Scores below 8 require a repair. |
| Platform portability | Mapping between source and target runtime features. | Unsupported features and losses must be documented. |
| Forge packet | Structured artifact containing mode, platform, playbook, rubric, tests, and risks. | Validated by `scripts/validate_forge_packet.py`. |

## Quality Metrics

| Metric | Target | How To Measure |
|---|---|---|
| Playbook completeness | 100% | Required sections present or omission documented. |
| Source grounding | 100% | Allowed sources and unsupported behavior present. |
| Rubric coverage | 100% | All criteria scored with repairs when needed. |
| Test coverage | 3 required classes | Happy path, edge case, adversarial. |
| Porting transparency | 100% for port mode | Mapped features, unsupported features, and losses listed. |

## Anti-Patterns

| Anti-Pattern | Why It Fails | Deterministic Alternative |
|---|---|---|
| Generic role | Produces weak behavior. | Composite archetype with boundaries. |
| Hidden reasoning request | Can leak internal reasoning. | Concise rationale or decision trace. |
| Unbounded web claims | Platform data can drift. | User-provided or dated source only. |
| Output-contract drift | Breaks downstream consumers. | Preserve schema or document intentional revision. |
| Same text across platforms | Ignores runtime differences. | Use platform portability matrix. |

## References

- `assets/prompt-forge-checklist.md`
- `assets/playbook-contract.json`
- `assets/platform-portability-matrix.json`
- `references/evaluation-rubric.md`
