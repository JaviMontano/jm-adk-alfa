# Local State Preservation Scripts

This directory contains deterministic local automation for
`local-state-preservation`.

## Contract

- `validate_local_state_preservation.py` validates preservation report JSON
  offline.
- `check.sh` runs valid and invalid fixture cases without network, time, or
  randomness.
- Fixtures in `fixtures/` include passing reports and negative mutations.
- Scripts do not mutate repository files.

## Validate

```bash
bash skills/local-state-preservation/scripts/check.sh
```
