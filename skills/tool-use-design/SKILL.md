---
name: tool-use-design
version: 1.0.0
description: "Disenar descripciones de tools como contrato de routing y aplicar la estrategia de built-in tools grep then read then edit."
owner: "JM Labs"
triggers:
  - tool use design
  - tool description contract
  - builtin tool strategy
  - tool routing
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Tool Use Design

## Capacidad

Diseñar la descripción de cada tool como un **contrato de routing** que el modelo lee para decidir, sin contexto adicional, cuándo invocarla y con qué forma de entrada; y aplicar la estrategia canónica de built-in tools `Grep → Read → Edit` para operar sobre repositorios sin saturar la ventana. La descripción no es documentación humana: es la única señal que recibe el planner para discriminar entre tools que compiten. Una frontera recíproca bien escrita (cada descripción dice qué hace y qué NO hace, delegando explícitamente en su vecina) elimina ambigüedad de selección.

## Cuándo usarla

- Estás definiendo o refactorizando el tool surface de un agente y dos tools se solapan en propósito (overloading).
- El agente elige el tool equivocado o pide aclaración cuando la decisión debería ser inmediata.
- Una descripción genérica del tipo `"Analyzes content"` no permite al modelo saber qué entrada espera ni dónde está su frontera.
- Vas a operar sobre un repo desconocido y necesitas un protocolo de lectura que evite el `read-all` masivo.
- Edit falla de forma intermitente (anchor no único) y falta un fallback documentado.

## Cómo construir

1. **Inventaria el tool surface** y detecta solapamientos: dos tools que un humano podría confundir son dos tools que el modelo confundirá.
2. **Escribe cada descripción como contrato**: propósito en una frase, **input format** explícito, 1–2 ejemplos de invocación y la **frontera** ("usa X para A; para B usa Y").
3. **Resuelve el overloading con rename + split**, no con prosa: un tool sobrecargado se divide en dos con nombres y fronteras recíprocas, en lugar de explicar matices en un párrafo.
4. **Documenta el failure mode de Edit**: el anchor (`old_string`) debe ser único; si no lo es, Edit falla. Declara el **fallback Read+Write** para reescritura total cuando el anchor no se puede aislar.
5. **Codifica la estrategia de built-in tools** `Grep → Read → Edit`: localizar con Grep/Glob, leer solo los archivos relevantes con Read, mutar con Edit. **Nunca** un `Glob("**/*") + Read all` upfront.
6. **Valida con el checklist** antes de cerrar: fronteras recíprocas, decisión de tool inmediata, sin lectura masiva.

## Patrón correcto

```python
# GOOD — descripciones como contrato con frontera recíproca + estrategia Grep→Read→Edit
TOOLS = [
    {
        "name": "search_code",
        "description": (
            "Find files or symbols by pattern across the repo. "
            "Input: a regex or literal string. Returns matching paths + line numbers. "
            "Use this FIRST to locate. To read a known file's contents, use read_file instead."
        ),
    },
    {
        "name": "read_file",
        "description": (
            "Read the full contents of ONE known file path. "
            "Input: an absolute path. Use after search_code has located the file. "
            "Do NOT use to discover files — that is search_code's job."
        ),
    },
    {
        "name": "edit_file",
        "description": (
            "Replace an exact, UNIQUE anchor string in a file. "
            "Input: path, old_string (must be unique), new_string. "
            "FAILS if old_string is not unique. Fallback: read_file then write_file for a full rewrite."
        ),
    },
]

# Workflow the descriptions enforce: locate cheaply, read selectively, mutate precisely.
hits = search_code(pattern="def handle_payment")   # Grep
src = read_file(path=hits[0].path)                  # Read only the relevant file
edit_file(path=hits[0].path, old_string=unique_anchor, new_string=patched)  # Edit
```

## Anti-patrón

```python
# ANTI — descripciones genéricas + read masivo upfront
TOOLS = [
    {"name": "analyze", "description": "Analyzes content."},        # no input, no frontera
    {"name": "process", "description": "Processes the file."},      # solapa con analyze
]

# El agente, sin frontera, no sabe cuál elegir → pide aclaración o adivina.
# Y para "entender el repo" carga todo en contexto:
all_files = glob("**/*")
context = "".join(read_file(p) for p in all_files)  # ~200k tokens, satura la ventana
# Edit sin fallback documentado: si el anchor no es único, falla en silencio.
```

## Checklist de validación

- ¿Cada descripción declara input format + 1–2 ejemplos + frontera recíproca con su vecina?
- ¿El overloading se resolvió con rename + split, no con un párrafo explicativo?
- ¿El modelo puede elegir el tool correcto por decisión rápida, sin pedir aclaración?
- ¿Está documentado el failure mode de Edit (anchor no único) y su fallback Read+Write?
- ¿La estrategia es `Grep → Read → Edit`, sin ningún `Glob("**/*") + Read all` upfront?

## Katas y skills relacionadas

- Katas: `katas-21`, `katas-23`.
- Skills: `katas-tool-description-quality`, `katas-builtin-tool-selection`.
