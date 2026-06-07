# Git Workflow - Body of Knowledge

## Canon

Git workflow guidance starts with repo state. A safe plan never assumes a clean tree, current base branch, passing checks, or permission to run destructive commands.

## Workflow Decisions

| Decision | Safe Default | Stop Condition |
|----------|--------------|----------------|
| Base update | `git pull --ff-only origin main` | non-fast-forward required |
| Branching | `codex/<purpose>` or project pattern | invalid slug or protected base mutation |
| Commit | conventional or project-local convention | unvalidated changes |
| PR | ready only after local validation | open conflicting PR or failed checks |
| Merge | squash unless project policy differs | CI failure or review block |
| Release tag | SemVer tag with evidence | missing version source or dirty tree |
| Conflicts | inspect, resolve, validate, commit | unresolved markers or failed tests |

## Quality Metrics
| Metric | Target | How to Measure |
|--------|--------|---------------|
| Repo-state coverage | 100% | branch, cleanliness, alignment, open PRs |
| Command safety | 100% | no forbidden destructive commands |
| Validation coverage | 100% | local checks and CI/PR gates named |
| Cleanup coverage | 100% | branch deletion and main update named when merging |
| Evidence coverage | 100% | observed state and assumptions tagged |

## References
- `assets/workflow-plan-contract.json`
- `assets/command-policy.json`
- `assets/branch-policy.json`
- `assets/release-policy.json`
