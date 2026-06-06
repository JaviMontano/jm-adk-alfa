# Ideate Component - Body of Knowledge

## Canon

Component ideation happens before design or implementation. The output should decide whether a proposed plugin component deserves to exist, what it should be called, where it belongs, and what it depends on.

## Component Types

| Type | Use for | Boundary |
|------|---------|----------|
| Skill | Multi-step work with quality criteria and edge cases | Does not only route another component |
| Agent | Coordination across multiple skills or decisions | Does not manage a single trivial skill |
| Command | User-facing invocation or alias | Does not duplicate command content |
| Hook | Lifecycle automation | Must use a compatible hook type/event pair |

## Quality Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Candidate count | 2-3 | Concept card candidates list |
| Name safety | 100% | Kebab-case and no existing-name conflict |
| Relationship coverage | 100% | Direct dependencies, consumers, and diagram present |
| Conflict resolution | 100% | none, merge, split, differentiate, create-dependency, or accept-isolated |
| MOAT fit | 100% | Depth matches complexity score and required assets |
| Evidence coverage | 100% | Summary, inventory, conflicts, validation, and risks carry evidence tags |

## References

- `references/component-patterns.md`
- `assets/component-type-policy.json`
- `assets/moat-depth-policy.json`
