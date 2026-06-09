# red-y-referencias

Deterministic management for professional references and referral follow-ups. The skill builds a privacy-safe packet from supplied evidence, tracks explicit consent, computes stale follow-ups from an `as_of` date, and blocks unauthorized contact actions.

## Offline Validation

```bash
bash skills/red-y-referencias/scripts/check.sh
python3 -B scripts/validate-skill-dod.py --skill red-y-referencias
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill red-y-referencias
```

## Determinism Rules

- Require explicit consent before any contact or reference action.
- Compute follow-up age only from packet `as_of`; never use the current clock.
- Require ISO `YYYY-MM-DD` dates.
- Keep direct email, phone, payment, and private channel details out of packets.
- Validate JSON packets with `scripts/reference_network_validator.py`.
