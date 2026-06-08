# Body of Knowledge

## Maintenance Shape

Alfa maintenance is safest when treated as a pipeline, not as a broad cleanup pass. Bootstrap proves the repo, repo-sync-audit proves the baseline, local-state-preservation protects human work, branch-plan scopes mutation, import-consolidation-plan limits drift, cleanup-plan controls transients, validation-gates prove safety, and closeout records what remains.

## Branch Policy

Mutating work must run on an isolated branch. `main` is a baseline and integration target, not the working surface. This keeps old branches, generated indexes, and cleanup moves from collapsing into a single hard-to-review diff.

## Preservation Policy

Any operation that can move, delete, archive, regenerate, import, or rewrite files requires a preservation manifest first. The orchestrator does not implement preservation itself; it requires the `local-state-preservation` packet.

## Cleanup Policy

Cleanup without a manifest is not cleanup; it is untracked loss. Every transient file action needs original path, destination, decision, and validation evidence.
