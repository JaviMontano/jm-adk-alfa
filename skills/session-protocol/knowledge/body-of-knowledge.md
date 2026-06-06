# Session Protocol - Body of Knowledge

## Purpose

Session protocol is the continuity gate before accepting new work. It loads
context, recovers state, proposes pending closure, and asks for confirmation.

## Required Phases

| Phase | Output | Blocker |
|---|---|---|
| Context Loading | ordered source list | required source missing without `[OPEN]` |
| State Recovery | recent changes, open tasks, git/spec state | contradictory state unresolved |
| Pending Closure | close/continue/defer/archive recommendations | auto-closure without confirmation |
| Next Steps | 2-3 ranked next steps | work starts before user direction |

## Closure Recommendations

- `close`: evidence indicates the task is complete.
- `continue`: task remains aligned and active.
- `defer`: task is valid but not current priority.
- `archive`: task is stale or no longer relevant.

## Anti-Patterns

- Skipping context loading.
- Starting implementation before confirmation.
- Auto-closing stale tasks.
- Hiding missing changelog or tasklog.
- Treating changelog/tasklog conflicts as resolved.

## Quality Metrics

| Metric | Target | How To Measure |
|---|---:|---|
| Context order coverage | 100% | ordered source list present |
| Pending item coverage | 100% | open items reviewed or source gap marked |
| Closure confirmation | 100% | no automatic close/archive |
| Next-step count | 2-3 | ranked recommendations |
