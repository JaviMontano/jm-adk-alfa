# Scripts

- `plan_30_60_90.py --input <json>` validates sustainable 30/60/90 plan packets.
- `check.sh` runs deterministic valid, blocked, and invalid fixtures.

Exit codes:

- `0`: valid sustainable plan.
- `1`: blocked or invalid plan.
- `3`: missing input file or invalid JSON.
