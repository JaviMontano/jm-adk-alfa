# Discovery Orchestration — Body of Knowledge

## Canon
- Discovery orchestration is a dependency-aware pipeline, not a checklist. [DOC]
- Phase transitions require quality gates with measurable pass/block criteria.
  [DOC]
- Deliverables are not complete until an owner, source skill, status, validation
  evidence, and next action are recorded. [DOC]
- Parallel execution is allowed only when dependency edges do not conflict.
  [DOC]
- A blocked pipeline is valid only when blockers and next actions are explicit.
  [DOC]

## Canonical Packet Sections

| Section | Purpose |
|---------|---------|
| `pipeline` | ID, scope, status, exit criteria |
| `phases` | Ordered discovery phases and skills |
| `dependencies` | Skill-to-skill dependency edges |
| `gates` | Quality gates between phases |
| `deliverables` | Owner-bound deliverable register |
| `blockers` | Explicit blockers and next actions |
| `validation` | Evidence that sequencing/gates are valid |
| `risks` | Remaining orchestration risks |

## Quality Metrics
| Metric | Target | How to Measure |
|--------|--------|---------------|
| Dependency integrity | 100% | Graph has no cycles |
| Gate coverage | 100% | Every phase transition has a gate |
| Deliverable ownership | 100% | Every deliverable has owner and source skill |
| Ready-state quality | 100% | Ready pipelines have passing gates and validated deliverables |
| Evidence coverage | 100% | Claims include allowed evidence tags |

## Anti-Patterns

- Running all discovery skills in parallel without dependency checks. [DOC]
- Calling a deliverable complete before validation. [DOC]
- Gate criteria such as "looks good" or "stakeholders agree later". [DOC]
- Blockers without owners or next actions. [DOC]

## References
- `assets/pipeline-schema.json`
- `assets/gate-policy.json`
- `assets/deliverable-policy.json`
- `assets/dependency-policy.json`
- `assets/status-taxonomy.json`
- `assets/report-contract.json`
