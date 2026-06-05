# Scripts

`validate_bmad_packet.py` validates deterministic BMAD output packets and artifact-chain fixtures.

## Usage

```bash
python3 -B skills/bmad-method/scripts/validate_bmad_packet.py \
  --contract skills/bmad-method/assets/bmad-packet-contract.json \
  --packet skills/bmad-method/scripts/fixtures/valid-greenfield-packet.md \
  --scenario greenfield \
  --expect pass
```

Run all fixtures:

```bash
bash skills/bmad-method/scripts/check.sh
```
