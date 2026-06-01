# Folio Generator Review

## Verdict

`folio-generator` meets the current one-skill Definition of Done.

## Evidence

- `python3 -B scripts/validate-skill-dod.py --skill folio-generator` passes.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill folio-generator` passes.
- `python3 -B scripts/validate-skills.py --strict` passes.
- Assets are declared in `skills/folio-generator/assets/manifest.json`.
- Runtime rendering uses `skills/folio-generator/assets/folio-style.css`.

## Assets

- `assets/folio-style.css`
- `assets/brand-tokens.json`
- `assets/manifest.json`

## Remaining Catalog Work

The catalog still requires the same DoD pass skill by skill. This review certifies only `folio-generator`.
