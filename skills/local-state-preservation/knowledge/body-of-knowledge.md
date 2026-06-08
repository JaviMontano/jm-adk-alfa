# Body of Knowledge

## Preservation Surfaces

A repository cleanup can lose work even when `git status` looks simple. The preservation packet separates the local state into six surfaces: tracked changes, untracked files, ignored files, stashes, worktrees, and sibling clones. Each surface needs its own evidence because each can be lost by a different class of operation.

## Artifact Invariants

Preservation artifacts are useful only when they can be verified later. Every patch, archive, report, manifest, and checksum file must record its source paths, destination path, byte size, and SHA-256 digest. Missing metadata converts an archive into an opaque blob and should block cleanup.

## Private Boundary

Private context such as `user-context/jarvis-os` is inventory-only. A valid report may acknowledge that the path exists and is excluded, but must not preserve its payload into git-visible artifacts or publishable archives.

## Stash Boundary

Stashes are rollback points created by a human or another tool. The default policy is inventory-only. Applying, popping, dropping, or rewriting a stash is outside this skill unless the user explicitly asks for it.

## Cleanup Rule

No cleanup is considered safe unless every moved, archived, or deleted local artifact is represented in a manifest that includes original path, final destination, checksum, and decision rationale.
