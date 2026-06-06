# Session Manager — Body of Knowledge

## Canon

Session Manager maintains reproducible project state through local evidence. It
does not discover progress from memory, branch names, network services, or time.
The canonical source is `.specify/context.json`; the computed source is the
artifact set under `.specify/**`, `tasks.md`, `spec.md`, and feature tests.

## Stage Semantics

| Stage | Required Evidence | Next Action |
|---|---|---|
| `specified` | `spec.md` or `.specify/spec.md` | Create or recover a plan. |
| `planned` | `.specify/plans/plan-*.md` | Create or recover tests. |
| `testified` | feature test evidence | Create or recover tasks. |
| `tasks-ready` | `tasks.md` or `.specify/tasks.md` | Begin implementation with task evidence. |
| `implementing` | task evidence plus 1-99 percent progress | Continue or validate implementation. |
| `complete` | all tasks complete plus validation evidence | Persist completion and hand off. |

## Quality Metrics

| Metric | Target | How to Measure |
|---|---:|---|
| Source coverage | 100% | Required priming sources are loaded or marked `[OPEN]`. |
| Stage determinism | 100% | Computed stage follows `assets/stage-policy.json`. |
| Persistence safety | 100% | Writes are authorized and inside allowed `.specify/**` targets. |
| Offline validation | 100% | `bash skills/session-manager/scripts/check.sh` passes. |

## Anti-Patterns

- Creating `.specify/context.json` from defaults without authorization.
- Reporting `implementing` without task evidence.
- Jumping multiple stages in one pass.
- Marking `complete` without validation evidence.
- Treating a conversation summary as project-state evidence.
