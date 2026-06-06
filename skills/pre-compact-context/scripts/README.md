# Pre Compact Context Scripts

The scripts directory validates JSON pre-compaction packets offline.

## Commands

```bash
bash skills/pre-compact-context/scripts/check.sh
python3 -B skills/pre-compact-context/scripts/validate_pre_compact_packet.py \
  skills/pre-compact-context/scripts/fixtures/valid-pre-compact-packet.json
```

The checks accept valid packets and reject packets with dropped P0 context,
missing rehydration prompt, or leaked secrets. They do not use network,
wall-clock, random data, or files outside this skill directory.
