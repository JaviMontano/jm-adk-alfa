<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-multipass-prompt-chaining
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

Auditoría de 50 archivos `src/*.py` resuelta con chaining multi-pass: pase 1 tipado por archivo (paralelizado), pase 2 de integración solo sobre los resúmenes tipados.

## Result

### Pase 1 · resúmenes tipados por unidad (extracto)

```json
[
  {"file": "src/auth.py", "status": "ok", "findings": [{"severity": "high", "issue": "secret hardcodeado L42"}]},
  {"file": "src/parser.py", "status": "ok", "findings": []},
  {"file": "src/legacy.py", "status": "failed", "error": "SyntaxError: no parseable"}
]
```

### Pase 2 · informe integrado

- Unidades procesadas: 50 · válidas: 49 · fallidas: 1 (`src/legacy.py`).
- Hallazgos críticos agregados: 1 secreto hardcodeado en `src/auth.py` L42.
- El pase 2 consumió solo los 50 resúmenes tipados, nunca el contenido crudo de los archivos.

## Validation

- Skill activada intencionalmente (la tarea no cabe en single-pass).
- El estado de error tipado evitó la falla silenciosa: el informe reporta 49/50 válidas, no asume 50.
- El pase 2 nunca re-ingirió las unidades crudas; se respetó el límite de contexto por pase.

## Risks and Limits

- `src/legacy.py` quedó sin auditar por error de parseo; requiere reintento manual.
- No reemplaza revisión experta de seguridad de alto riesgo.
