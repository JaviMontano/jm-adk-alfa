# Find Skills — Body of Knowledge

## Canon

`find-skills` is a capability discovery and recommendation skill. It searches local catalogs first, optionally considers remote sources, scores every candidate with stable criteria, and never installs anything without explicit confirmation.

## Deterministic Rules

| Rule | Requirement |
|------|-------------|
| Source order | Local catalogs before remote sources unless the user says remote-only. |
| Remote evidence | Remote candidates require source URL and exact `remote_snapshot_date`. |
| Scoring | Every candidate must include `score_total` and rubric breakdown. |
| Bounded output | Default top 3; maximum 5 unless the user requests an audit. |
| Security | Tier F candidates cannot be selected. |
| Installation | `auto_install` must be false; present commands only. |
| Offline mode | Do not call network, `npx`, package managers, or current-time APIs. |

## Quality Metrics

| Metric | Target |
|--------|--------|
| Evidence coverage | 100 percent of claims |
| Candidate scoring | 100 percent of candidates |
| Candidate bound | 5 or fewer by default |
| Unsafe install actions | 0 |
| Remote undated claims | 0 |
| Offline validation | `scripts/check.sh` passes |
