# Session Start Bootstrap - Body of Knowledge

## Purpose

Session startup prevents unsafe work by proving the repo, branch, context, hard
rules, blockers, and first action before implementation begins.

## Startup Checks

| Check | Why It Matters | Evidence |
|---|---|---|
| Repo identity | Prevents edits in the wrong workspace | Path, marker, or git remote |
| Branch state | Prevents work on stale or wrong branch | `git status --short --branch` |
| Dirty tree | Protects user changes | changed path list |
| Open PR state | Enforces serial PR workflows | `gh pr list` or explicit source |
| Context sources | Avoids hidden memory dependence | path or command list |
| First action | Makes startup actionable | concrete command or edit target |

## Source Precedence

1. Explicit user config for this session.
2. Repo instructions and active AGENTS/CLAUDE files.
3. Prior ReleasePacket or rehydration packet.
4. Tasklog/changelog or review docs.
5. Inference from local state, tagged `[INFERENCE]`.

## Anti-Patterns

- Writing before checking dirty tree.
- Bulk-loading private context.
- Assuming a stale handoff is current.
- Starting the next PR while another PR is open.
- Omitting first action.
- Hiding missing repo or branch evidence.

## Quality Metrics

| Metric | Target | How To Measure |
|---|---:|---|
| Environment evidence | 100% | repo, branch, dirty state recorded |
| Context source listing | 100% | every loaded source is listed |
| Guardrail coverage | 100% | hard rules and stop criteria recorded |
| First-action clarity | 1 action | exact next command or file target |

## Failure Modes

- Dirty tree: block writes and preserve changed paths.
- Open PR: block if workflow requires one PR at a time.
- Missing handoff: proceed from repo instructions only with `[OPEN]` gap.
- Conflicting instructions: preserve both and apply source precedence.
