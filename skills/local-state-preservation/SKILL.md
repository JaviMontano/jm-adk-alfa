---
name: local-state-preservation
version: 1.0.0
description: "Preserves dirty local repository state before sync, cleanup, branch switching, imports, or archive operations by inventorying tracked changes, untracked files, ignored files, worktrees, stashes, private paths, patches, archives, checksums, and explicit non-touch decisions."
owner: "JM Labs"
triggers:
  - preserve local state
  - dirty tree preservation
  - before repo cleanup
  - archive local work
  - patch and tarball manifest
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Write
---

# Local State Preservation

Use this skill before repo sync, branch switching, imports, cleanup, archive moves, or any operation that could overwrite, move, publish, or invalidate local-only work.

## Required Result

Produce a preservation packet before mutating the repo:

- Dirty-state inventory: branch, HEAD, upstream, tracked changes, untracked files, ignored files, stashes, worktrees, nearby clones, and private paths.
- Preservation artifacts: patch files, archives, manifests, reports, or checksum files with SHA-256, size, source paths, and destination path.
- Explicit non-touch decisions for stashes and private paths.
- A validation report that passes `scripts/validate_local_state_preservation.py`.

The machine-readable report follows `assets/preservation-report-contract.json`. Use `templates/output.md` for the human closeout and `assets/preservation-template.md` for the JSON shape.

## Procedure

### 1. Establish Baseline

Run read-only checks first:

- `git status --short --branch`
- `git rev-parse --show-toplevel`
- `git rev-parse HEAD`
- `git remote -v`
- `git stash list`
- `git worktree list --porcelain`

If the repo root, branch, or upstream cannot be determined, stop before writes and record the blocker.

### 2. Inventory Every Surface

Inventory six surfaces independently:

- `tracked_changes`: staged, unstaged, renamed, deleted, or conflicted tracked files.
- `untracked_files`: local files not in git.
- `ignored_files`: files hidden by `.gitignore`, including workspaces and local smoke-test outputs.
- `stashes`: list only by default; do not pop, apply, drop, or rewrite.
- `worktrees`: sibling worktrees and their branch/dirty state.
- `clones`: sibling clones that could contain divergent local work.

Use `assets/surface-inventory-policy.json` for required fields.

### 3. Preserve Before Mutation

For tracked changes, create a patch. For untracked and ignored files, create an archive or manifest-backed move into an explicitly allowed archive/workspace root. For worktrees and clones, preserve enough evidence to recreate the state without rewriting those repos.

Every preservation artifact must include:

- `path`: location of the artifact.
- `destination_path`: final preservation target.
- `kind`: `patch`, `archive`, `manifest`, `report`, or `checksum`.
- `source_paths`: one or more original paths.
- `sha256`: 64-character lowercase or uppercase hex digest.
- `size_bytes`: positive integer.

Use `assets/archive-manifest-policy.json` for the artifact contract.

### 4. Enforce Private Boundaries

Never publish, move into git, or include artifact payloads for private paths such as `user-context/jarvis-os`. Record them as excluded private context with a reason and a non-touch decision.

Use `assets/private-path-policy.json` and include `scope.private_path_exclusions` in the report.

### 5. Record Non-Touch Decisions

The report must explicitly state that stashes are inventory-only unless the user gave a direct instruction to alter them. Private paths must be marked do-not-move-or-publish.

Use `assets/non-touch-policy.json` for the required wording and decision surfaces.

### 6. Validate

Run the offline contract check:

```bash
python3 skills/local-state-preservation/scripts/validate_local_state_preservation.py <report.json>
```

For the skill's deterministic fixtures, run:

```bash
bash skills/local-state-preservation/scripts/check.sh
```

Do not claim the state is preserved unless the validator passes or the remaining failure is explicitly reported as a blocker.

## Blocking Conditions

Fail closed when:

- Any artifact lacks `sha256`, `source_paths`, `destination_path`, or positive `size_bytes`.
- A preserved artifact includes `user-context/jarvis-os` or another declared private path.
- Stashes are touched, or the report omits the stash non-touch decision.
- Cleanup or archive actions have no manifest.
- The report claims `validation.status: pass` without command evidence.

## Related Skills

- `repo-sync-auditor`
- `workspace-governance`
- `git-workflow`
- `safe-scripting-and-bash`
- `quality-gatekeeper`
- `session-end-cleanup`
