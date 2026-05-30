<!--
generated-by: scripts/scaffold-skill.py
generated-for: structured-output-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Structured Output Design Output

## Resumen

{summary}

## Inventario de campos

| Campo | Presencia | Modelado |
|---|---|---|
| {campo} | garantizado / ocasional | `required` / `["tipo","null"]` / enum+`'other'` |

## Schema propuesto

```python
{schema_code}
```

## Patrón GOOD (llamada + parseo)

```python
{good_code}
```

## Anti-patrón reemplazado

```python
{anti_code}
```

## Checklist de validación

- [ ] `required` = presencia real en la fuente
- [ ] Opcionales `nullable`, sin defaults `''`/`0`/`"N/A"`
- [ ] Enums cerrados con `'other'`+`details`
- [ ] `tool_choice` forzado solo sin decisión de tool
- [ ] Consumidor parsea desde `tool_use.input`
- [ ] Salida validada contra schema; fallo -> retry/escalada

## Evidencia

{evidence}

## Riesgos y límites

{risks}
