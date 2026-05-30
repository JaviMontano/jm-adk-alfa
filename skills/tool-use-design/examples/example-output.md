<!--
generated-by: scripts/scaffold-skill.py
generated-for: tool-use-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

Las tres descripciones genéricas se reescriben como contratos con frontera recíproca y se codifica el flujo `Grep → Read → Edit`, con fallback Read+Write para `modify` cuando el anchor no es único.

## Evidence

Síntoma confirmado: `read: "Reads code."` no declara que recibe UN path conocido, así que el modelo lo usaba para descubrir archivos y caía en read-all. Las tres descripciones carecen de input format y frontera.

## Result

```python
# GOOD — descripciones-contrato con frontera recíproca
TOOLS = [
    {
        "name": "search_code",
        "description": (
            "Find files or symbols by pattern across the repo. "
            "Input: a regex or literal string. Returns paths + line numbers. "
            "Use FIRST to locate. To read a known file, use read_file instead."
        ),
    },
    {
        "name": "read_file",
        "description": (
            "Read the full contents of ONE known file path. "
            "Input: an absolute path. Use after search_code located it. "
            "Do NOT use to discover files — that is search_code's job."
        ),
    },
    {
        "name": "edit_file",
        "description": (
            "Replace an exact, UNIQUE anchor string in a file. "
            "Input: path, old_string (unique), new_string. "
            "FAILS if old_string is not unique. Fallback: read_file then write_file for a full rewrite."
        ),
    },
]

hits = search_code(pattern="def handle_payment")  # Grep
src = read_file(path=hits[0].path)                 # Read solo lo relevante
edit_file(path=hits[0].path, old_string=unique_anchor, new_string=patched)  # Edit
```

## Anti-pattern evitado

```python
# ANTI — lo que hacía antes el agente
TOOLS = [{"name": "search", "description": "Searches the codebase."}]  # sin input ni frontera
context = "".join(read_file(p) for p in glob("**/*"))  # ~200k tokens, satura la ventana
```

## Validation

- [x] Cada descripción: input format + ejemplo + frontera recíproca (search↔read↔edit).
- [x] Overloading resuelto con rename (`read` → `read_file`) + frontera explícita.
- [x] Routing inmediato: localizar = search_code, leer conocido = read_file.
- [x] Edit failure mode (anchor no único) + fallback Read+Write documentados.
- [x] Flujo `Grep → Read → Edit`, sin `Glob("**/*") + Read all`.

## Risks and Limits

- Si dos símbolos comparten nombre, `search_code` devuelve varios hits: el agente debe elegir por path antes de leer.
- El fallback Read+Write de `edit_file` reescribe el archivo completo; usar solo cuando no exista un anchor aislable.
