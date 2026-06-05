# Scripts

`validate_assembly_contract.py` validates deterministic assembly mode selection and Assembly Report Markdown packets.

## Report Validation

```bash
python3 -B skills/assembly-skill/scripts/validate_assembly_contract.py \
  --contract skills/assembly-skill/assets/assembly-report-contract.json \
  --report skills/assembly-skill/scripts/fixtures/valid-standard-report.md \
  --mode standard \
  --expect pass
```

## Mode Selection Validation

```bash
python3 -B skills/assembly-skill/scripts/validate_assembly_contract.py \
  --policy skills/assembly-skill/assets/mode-policy.json \
  --scorecard skills/assembly-skill/scripts/fixtures/scorecard-polish.json \
  --expect-mode deep
```
