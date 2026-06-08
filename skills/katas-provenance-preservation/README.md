# Katas Provenance Preservation

Kata para preservar provenance tipada en reportes factuales. El invariante central es simple: no hay `claim` sin `sources[]`, y cada `source_id` debe existir en `source_registry`.

## Triggers

- provenance preservation
- claim source mapping
- conflict flag
- source provenance

## Use When

- Un reporte agrega hechos desde varias fuentes.
- Subagentes paralelos aportan datos que deben auditarse claim por claim.
- Dos fuentes pueden contradecirse.
- El output debe evitar prosa libre sin trazabilidad.

## Output Contract

El entregable debe incluir:

- `source_registry[]` con `source_id`, `source_name` y `publication_date`.
- `claims[]` con `claim_id`, `claim`, `sources[]` y `conflict`.
- Conflictos preservados con ambas posturas y `needs_human_review=true`.
- Validación estructural: cero claims sin fuentes y cero source refs desconocidos.

## Offline Validation

```bash
bash skills/katas-provenance-preservation/scripts/check.sh
python3 -B skills/katas-provenance-preservation/scripts/validate_provenance_preservation.py skills/katas-provenance-preservation/scripts/fixtures/valid-company-report.json
```
