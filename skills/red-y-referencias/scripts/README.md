# Scripts

## reference_network_validator.py

Validates a deterministic reference-network packet JSON file. It checks schema, evidence references, explicit consent, allowed actions, follow-up cadence from packet `as_of`, network edges, privacy boundaries, duplicate IDs, and offline validation flags.

```bash
python3 skills/red-y-referencias/scripts/reference_network_validator.py --input skills/red-y-referencias/scripts/fixtures/valid-consented-reference.json
```

## check.sh

Runs valid, blocked, and invalid fixtures offline. Expected result: valid fixtures exit `0`; blocked and invalid fixtures exit non-zero.
