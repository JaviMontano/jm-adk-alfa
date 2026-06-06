# Workspace Governance Scripts

`check.sh` validates deterministic workspace governance report fixtures offline.

Run from the repository root:

```bash
bash skills/workspace-governance/scripts/check.sh
```

The validator accepts `jm-labs.workspace-governance.report.v1` packets and
rejects missing gitignore coverage, invalid session names, missing READMEs,
unflagged stale sessions, bad task bridges, and unsafe action targets.
