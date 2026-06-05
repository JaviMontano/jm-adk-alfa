# Output Contract Enforcer

`output-contract-enforcer` validates generated artifacts against declared contracts and blocks non-conformant outputs.

## Triggers

- `/jm:verify`
- "Validate this output against its contract"
- "Check required sections"
- "Does this JSON packet match the schema?"
- "Confirm evidence tags and naming"

## Minimum Inputs

- Contract source or explicit required fields.
- Generated output or file path.
- Output type: markdown, json, html, or unknown.
- Evidence-tag requirement.
- Naming policy when a file path is involved.

## Output

The skill returns a deterministic validation packet with `status`, `checks`, `violations`, `repair_suggestions`, and `evidence`.

## Deterministic Gate

```bash
bash skills/output-contract-enforcer/scripts/check.sh
python3 -B scripts/validate-skill-dod.py --skill output-contract-enforcer
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill output-contract-enforcer
```
