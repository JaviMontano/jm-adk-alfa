<!--
generated-by: codex/skill-script-determinism
generated-for: folio-generator
overwrite-policy: manual
-->

# Folio Generator Scripts

Deterministic local automation for reserving folio numbers.

## Entry Points

- `next-folio-number.sh`: calculates the next `PREFIX-YYYY-NNN` folio.
- `render-folio-html.py`: renders `templates/folio-template.html` with `assets/folio-style.css` and JSON data.
- `check.sh`: validates dry-run behavior, apply behavior, fixtures, and invalid-prefix handling.

## Contract

- Default mode is `--dry-run`; it prints the next folio and never creates or mutates the tracker.
- `--apply` is required to update `.folio-tracker.json`.
- `--date YYYY-MM-DD` makes the year deterministic for tests.
- `--tracker FILE` isolates state for fixtures or workspace-specific trackers.
- Tracker reads/writes use JSON parsing and atomic replace, not grep/sed rewrites.
- Rendering uses bundled assets and writes only when `--output` is explicit.

## Examples

```bash
bash skills/folio-generator/scripts/next-folio-number.sh --dry-run --date 2026-05-31 --tracker skills/folio-generator/scripts/fixtures/tracker.json COT
bash skills/folio-generator/scripts/next-folio-number.sh --apply COT
python3 skills/folio-generator/scripts/render-folio-html.py --data skills/folio-generator/scripts/fixtures/render-data.json
```
