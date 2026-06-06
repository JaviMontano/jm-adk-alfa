# Session Start Bootstrap Scripts

The scripts directory validates JSON startup packets offline.

## Commands

```bash
bash skills/session-start-bootstrap/scripts/check.sh
python3 -B skills/session-start-bootstrap/scripts/validate_session_start_packet.py \
  skills/session-start-bootstrap/scripts/fixtures/valid-start-packet.json
```

The checks accept clean and blocked startup packets and reject missing
environment, dirty-pass, and missing-first-action packets.
