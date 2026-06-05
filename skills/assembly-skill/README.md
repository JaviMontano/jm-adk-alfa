# Assembly Skill

`assembly-skill` orchestrates one target skill through diagnostic, intervention, certification, and optional trigger optimization.

## Activation

Use it for skill-quality pipeline requests such as x-ray plus surgeon plus certify, "make this skill production-ready", or "assembly-line this skill".

Do not use it for non-skill assembly work.

## Deterministic Resources

- `assets/mode-policy.json`: exact quick/standard/deep selection.
- `assets/assembly-report-contract.json`: report requirements.
- `assets/assembly-report-template.md`: canonical report shape.
- `assets/phase-gate-checklist.md`: manual gate checklist.
- `scripts/validate_assembly_contract.py`: offline report and mode validator.

## Required Gates

- One skill path only.
- No writes before Gate B.
- Quick mode is diagnostic-only.
- Standard and deep modes require post-intervention certification evidence.
- Deep mode records trigger metrics and re-certifies.

## Local Checks

```bash
bash skills/assembly-skill/scripts/check.sh
python3 -B scripts/validate-skill-dod.py --skill assembly-skill
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill assembly-skill
```
