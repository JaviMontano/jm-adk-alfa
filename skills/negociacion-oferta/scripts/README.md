# Scripts

- `score_oferta.py --input <json>` validates and scores offer packets.
- `check.sh` runs deterministic valid, blocked, and invalid fixtures.

Exit codes:

- `0`: at least one offer passes every acceptance filter.
- `1`: packet issues or no offer passes every filter.
- `3`: bad input path or invalid JSON.
