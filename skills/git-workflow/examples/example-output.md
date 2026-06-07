# Example Output

## Repo State

- Branch: `main` [EXPLICIT]
- Clean tree: `true` [EXPLICIT]
- Base aligned: `true` [EXPLICIT]
- Open PRs: `0` [EXPLICIT]
- Decision: `proceed` [INFERRED]

## Branch Strategy

- Type: `feature` [INFERRED]
- Branch name: `codex/add-report-export` [EXPLICIT]
- Base branch: `main` [EXPLICIT]

## Command Plan

| Step | Command | Preconditions | Expected Outcome | Rollback |
|------|---------|---------------|------------------|----------|
| 1 | `git fetch origin main` | network available | remote base refreshed | retry or block on network failure |
| 2 | `git checkout -b codex/add-report-export origin/main` | clean tree | branch starts from remote main | delete branch before changes |
| 3 | `git status --short --branch` | branch created | confirms branch and cleanliness | block if dirty |
| 4 | `git add <scoped-files>` | validation ready | staged scoped changes | `git restore --staged <scoped-files>` |
| 5 | `git commit -m "feat: add report export"` | staged changes validated | conventional commit created | amend or revert before push |
| 6 | `git push -u origin codex/add-report-export` | commit exists | remote branch available for PR | delete remote branch if PR is abandoned |

## Commit and PR Policy

- Commit convention: `conventional` [CONFIG]
- Required checks: local checks plus CI Quality Gates [CONFIG]
- Merge method: `squash` [CONFIG]
- Delete branch after merge: `true` [CONFIG]

## Conflict and Release Policy

- Conflict strategy: fetch, rebase only if project policy allows, resolve markers, rerun validation, then push. [CONFIG]
- Release tag: `none` [CONFIG]

## Validation

- Run local checks before PR and block on failure. [CONFIG]
- Run `git diff --check` before commit. [CONFIG]

## Risks

- The plan assumes the named branch does not already exist remotely. [SUPUESTO]
