# Katas Tool Description Quality

Kata para convertir descripciones de tools en contratos de seleccion no solapados. Una descripcion valida declara input format, ejemplo de query y frontera explicita reciproca con tools vecinos.

## Use

Usa esta skill cuando:

- dos o mas tools compiten por el mismo turno
- el modelo responde bien pero con el tool incorrecto
- un tool multimodo necesita split
- un nombre de tool induce routing ambiguo
- el system prompt sesga la seleccion por keywords

## Contract

El contrato deterministico vive en `assets/`. Reportes JSON pueden validarse offline con:

```bash
bash skills/katas-tool-description-quality/scripts/check.sh
python3 -B skills/katas-tool-description-quality/scripts/validate_tool_description_quality.py <report.json>
```

## Output

Un reporte completo incluye evidencia de solapamiento, tools reescritos, decisiones de rename/split, fronteras reciprocas, validacion de misroute esperado y decision Guardian.
