---
name: katas-builtin-tool-selection
version: 1.0.0
description: "Seleccion de built-in tools con estrategia Grep then Read then Edit, failure modes y sin Read masivo upfront."
owner: "JM Labs"
triggers:
  - builtin tool selection
  - grep read edit
  - tool strategy
  - edit anchor
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Katas Builtin Tool Selection

## Qué es

Claude Code expone un conjunto de built-in tools, cada una con un uso primario y un failure mode:

- `Grep`: busca contenido por regex sobre el cuerpo de los archivos.
- `Glob`: busca paths por patrón de nombre (no mira contenido).
- `Read`: carga un archivo concreto en contexto.
- `Edit`: modificación dirigida sobre un anchor de texto único.
- `Write`: sobrescribe un archivo completo.
- `Bash`: ejecuta comandos de shell.

La estrategia incremental canónica es `Grep` → `Read` → `Edit`: buscar primero los entry points por contenido, leer selectivamente siguiendo imports, y aplicar una modificación puntual.

## Por qué importa (falla que evita)

Hacer `Read` sobre todo el repositorio carga miles de tokens innecesarios y quema el presupuesto de contexto. Un `Edit` con un anchor que no es único (matchea varias líneas) o que no existe simplemente falla. Saber qué tool aplica en cada momento es mecánica básica del examen y separa a los agentes eficientes de los que desperdician contexto en cada turno.

## Modelo mental

- `Grep` = buscar contenido. `Glob` = buscar paths. `Read` = cargar archivo. `Edit` = mod puntual. `Write` = reescribir. `Bash` = shell.
- Estrategia: `Grep` primero (encontrar entry points) → `Read` selectivo (seguir imports) → `Edit`/`Write` puntual.
- Failure mode de `Edit`: anchor no único o inexistente → falla. Fallback: `Read` entero + `Write` completo.
- Nunca "leer todo el repo upfront": eso es el anti-patrón que destruye el presupuesto de tokens.

## Patrón correcto

```python
matches = grep(pattern="processRefund\\(", glob="**/*.py")
content = read(matches[0].path)
edit(
    path=matches[0].path,
    old_text="if amount > 1000:",
    new_text="if amount > MAX_REFUND:",
)
```

## Anti-patrón

```python
all_files = glob("**/*")
for f in all_files:
    read(f)  # 200k tokens cargados sin necesidad

edit(old_text="if amount", ...)  # múltiples líneas matchean → falla
```

## Argumento de certificación

- Escoger el tool correcto en una decisión rápida según uso primario.
- Describir el failure mode de `Edit` (anchor no único/inexistente) y su fallback `Read` + `Write`.
- Defender la estrategia `Grep` → `Read` → `Edit`.
- Rechazar el `Read` masivo upfront sobre el repositorio.
- Emitir reportes críticos compatibles con `assets/builtin-tool-selection-report-contract.json`.
- Validar tool-fit, economía de lectura y seguridad de anchor con `scripts/check.sh`.

## Contrato determinístico

La skill usa `assets/` como contrato offline:

- `assets/tool-fit-policy.json`: contenido usa `Grep`, paths usan `Glob`, lectura usa `Read`, edición dirigida usa `Edit`, fallback completo usa `Write`.
- `assets/read-economy-policy.json`: si el target es desconocido, buscar antes de leer; `Read` masivo upfront queda bloqueado.
- `assets/edit-anchor-policy.json`: `Edit` requiere `unique_match_count=1`; `Write` como fallback requiere lectura completa previa y razón explícita.
- `assets/evidence-policy.json`: evidencia local, sin red ni random.

Validación local:

```bash
bash skills/katas-builtin-tool-selection/scripts/check.sh
```

## Cuándo activar

- Cuando el agente debe explorar o modificar un codebase y necesita elegir entre `Grep`, `Glob`, `Read`, `Edit`, `Write` o `Bash`.
- Cuando un `Edit` falla por un anchor ambiguo y hay que decidir el fallback.
- Cuando un plan de exploración propone cargar el repositorio entero y hay que corregirlo.

## Skills relacionadas

- `katas-plan-mode-exploration`
- `katas-custom-commands-skills`
- `katas-hierarchical-claude-memory`
