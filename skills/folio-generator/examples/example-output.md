<!--
generated-by: scripts/scaffold-skill.py
generated-for: folio-generator
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

Folio calculado: `COT-2026-043`.

## Execution

- Dry-run: `scripts/next-folio-number.sh --dry-run --date 2026-05-31 --tracker <tracker> COT`
- Render: `scripts/render-folio-html.py --data <datos.json>`
- Assets used: `assets/folio-style.css`, `assets/brand-tokens.json`

## Result

Documento HTML con:

- Folio `COT-2026-043`
- Destinatario `Cliente Ejemplo`
- Asunto `Propuesta de automatizacion documental`
- Total `COP 1.000.000`
- Firma `Javier Montano, Founder`

## Validation

- Dry-run no muta el tracker.
- Prefix `COT` cumple formato de tres letras mayusculas.
- HTML usa assets declarados en `assets/manifest.json`.
- Reserva final requiere confirmacion antes de `--apply`.
