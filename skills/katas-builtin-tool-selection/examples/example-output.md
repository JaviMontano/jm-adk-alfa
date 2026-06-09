<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-builtin-tool-selection
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

Estrategia `Grep` → `Read` → `Edit`: localicé `processRefund` por contenido, leí solo ese archivo y apliqué la modificación con un anchor único.

## Evidence

GOOD (patrón correcto):

```python
matches = grep(pattern="processRefund\\(", glob="**/*.py")
content = read(matches[0].path)
edit(
    path=matches[0].path,
    old_text="if amount > 1000:",
    new_text="if amount > MAX_REFUND:",
)
```

ANTI (lo que se evita):

```python
all_files = glob("**/*")
for f in all_files:
    read(f)  # 200k tokens cargados sin necesidad

edit(old_text="if amount", ...)  # múltiples líneas matchean → falla
```

## Result

`Edit` aplicado sobre el único archivo que define `processRefund`, reemplazando `if amount > 1000:` por `if amount > MAX_REFUND:`.

## Validation

- Tool elegido coincide con la intención: `Grep` para contenido, `Read` selectivo, `Edit` puntual.
- Sin `Read` masivo upfront: no se cargó el repositorio entero.
- Anchor de `Edit` único (`if amount > 1000:`), no el ambiguo `if amount`.
- Fallback definido: si el anchor no fuese único, `Read` entero + `Write` completo.

## Risks and Limits

- Si `processRefund` apareciera en más de un archivo, validar el `matches[0]` correcto antes de editar.
- Confirmar que `MAX_REFUND` está importada/definida en el módulo destino.

## Reporte JSON validable

```json
{
  "schema": "jm-labs.katas-builtin-tool-selection.report.v1",
  "skill": "katas-builtin-tool-selection",
  "objective": "Cambiar umbral hardcodeado sin leer el repo completo.",
  "scope": "Python repo",
  "selected_strategy": "Grep-Read-Edit",
  "tool_decisions": [
    {"intent": "content-search", "chosen_tool": "Grep", "rationale": "processRefund se localiza por contenido.", "evidence_tag": "[CODIGO]"},
    {"intent": "file-read", "chosen_tool": "Read", "rationale": "Sólo se lee el archivo matcheado.", "evidence_tag": "[CODIGO]"},
    {"intent": "targeted-edit", "chosen_tool": "Edit", "rationale": "El anchor es único.", "evidence_tag": "[CODIGO]"}
  ],
  "read_plan": {
    "mass_read_upfront": false,
    "search_before_read": true,
    "files_considered": 12,
    "files_read": ["src/payments/refund.py"]
  },
  "edit_plan": {
    "operation": "Edit",
    "anchor": {"old_text": "if amount > 1000:", "unique_match_count": 1},
    "fallback": {"declared": true, "action": "expand-anchor", "trigger": "", "full_file_read_before_write": false, "reason": "Expandir anchor si aparece duplicado."}
  },
  "evidence": [
    {"claim": "Grep precedió al Read.", "evidence_tag": "[CODIGO]", "source": "tool_decisions[0]"}
  ],
  "validation": {
    "status": "pass",
    "offline": true,
    "network_required": false,
    "deterministic": true,
    "uses_randomness": false,
    "checks": ["assets", "deterministic_scripts", "quality_criteria", "tool_fit", "read_economy", "edit_anchor_safety", "fallback_policy", "evidence_required"]
  },
  "risks": {"remaining": ["Confirmar import de MAX_REFUND."], "forbidden_patterns": []}
}
```
