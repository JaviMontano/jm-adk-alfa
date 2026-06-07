# Git Workflow Plan

## Repo State

- Branch: `{branch}`
- Clean tree: `{true|false}`
- Base aligned: `{true|false}`
- Open PRs: `{count}`
- Decision: `{proceed|block|clarify}`

## Branch Strategy

- Type: `{feature|hotfix|release|trunk}`
- Branch name: `{branch_name}`
- Base branch: `{base_branch}`

## Command Plan

| Step | Command | Preconditions | Expected Outcome | Rollback |
|------|---------|---------------|------------------|----------|
| `{n}` | `{command}` | `{precondition}` | `{outcome}` | `{rollback}` |

## Commit and PR Policy

- Commit convention: `{convention}`
- Required checks: `{checks}`
- Merge method: `{squash|merge|rebase}`
- Delete branch after merge: `{true|false}`

## Conflict and Release Policy

- Conflict strategy: `{strategy}`
- Release tag: `{none|semver-tag}`

## Validation and Risks

- Local validation: `{commands}`
- Stop conditions: `{conditions}`
- Risks: `{risks}`
