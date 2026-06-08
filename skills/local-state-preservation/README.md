# Local State Preservation

Preserves local repository state before sync, imports, branch switching, cleanup, or archive moves.

## Contract

The skill produces a preservation packet with:

- dirty-tree inventory
- untracked and ignored file inventory
- stash and worktree inventory
- private path exclusions
- patch/archive/report artifacts with SHA-256
- explicit non-touch decisions

The machine-readable report is validated by `scripts/validate_local_state_preservation.py`. The validator is offline and conservative: a missing checksum, missing source/destination path, private path artifact, or touched stash fails the report.

## Assets

- `assets/preservation-report-contract.json`
- `assets/surface-inventory-policy.json`
- `assets/archive-manifest-policy.json`
- `assets/private-path-policy.json`
- `assets/non-touch-policy.json`
- `assets/preservation-template.md`

## Deterministic Check

Run:

```bash
bash skills/local-state-preservation/scripts/check.sh
```
