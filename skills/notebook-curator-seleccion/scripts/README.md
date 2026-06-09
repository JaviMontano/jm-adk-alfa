# Scripts

- `validate_archetype.py --emit` prints canonical SEL-EMPRESA slots.
- `validate_archetype.py --input <json>` validates notebook source inventory offline.
- `check.sh` runs deterministic valid, blocked, and invalid fixtures.

Exit codes:

- `0`: complete archetype.
- `1`: blocked or invalid packet.
- `3`: missing input file or invalid JSON.
