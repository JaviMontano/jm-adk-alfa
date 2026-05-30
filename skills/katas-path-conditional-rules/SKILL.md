---
name: katas-path-conditional-rules
version: 1.0.0
description: "Reglas condicionales por glob de ruta; universales siempre cargadas, heuristicas de lenguaje on-demand."
owner: "JM Labs"
triggers:
  - path conditional rules
  - glob rules
  - conditional memory
  - per-path rules
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Katas Path Conditional Rules

## Qué es

Reglas heurísticas (estilo, lints, convenciones de lenguaje) que se cargan solo cuando el agente edita archivos que matchean un glob de ruta; las reglas universales (políticas de seguridad) permanecen siempre cargadas. La regla declara su glob de activación (`src/**/*.py`, `*.tf`): el agente carga la regla al entrar al archivo y la descarta al salir.

## Por qué importa (falla que evita)

Un `CLAUDE.md` que carga 2000 líneas para todos los archivos paga ese costo en todas las sesiones, incluso cuando el agente solo edita un README. Cargar reglas Python únicamente al tocar `*.py` libera contexto para el resto de la sesión. Sin esta clasificación, cada edición trivial arrastra heurísticas de lenguajes que no se están usando, inflando el contexto y degradando la atención.

## Modelo mental

- La regla declara su glob de activación: `src/**/*.py`, `*.tf`.
- El agente carga la regla al entrar a un archivo que matchea y la descarta al salir.
- Reglas grandes (heurísticas de lenguaje) → condicionales por glob.
- Reglas universales (políticas de seguridad) → siempre cargadas, sin glob.
- En conflictos puntuales por subpath, la regla más específica gana (precedencia por profundidad de ruta); ambas pueden coexistir cargadas.
- El ahorro es medible: comparar `input_tokens` editando un README contra editar un `.py`.

## Patrón correcto

```text
# <repo>/CLAUDE.md
@rules/security.md   # universal, siempre cargada

## When editing src/**/*.py:
@rules/python-style.md
@rules/python-testing.md

## When editing src/**/*.tf:
@rules/terraform.md
```

Resultado: `python-style.md` NO se carga al editar un README; `security.md` SÍ se carga siempre, en toda edición.

## Anti-patrón

```text
# <repo>/CLAUDE.md  — monolítico
@rules/python-style.md
@rules/python-testing.md
@rules/terraform.md
@rules/go-conventions.md
@rules/testing.md
@rules/security.md
# Todas cargan siempre, aunque solo edites un README.
```

Un único `CLAUDE.md` con todas las reglas (Python + Terraform + Go + Testing + Security) cargando en cada sesión paga el costo completo de tokens incluso para ediciones triviales.

## Argumento de certificación

Clasificar explícitamente cada regla como universal (siempre cargada, sin glob) o condicional por glob de ruta, y estimar el ahorro de tokens de forma medible:

- P1: una regla universal (seguridad) se carga directamente en el `CLAUDE.md` raíz, sin glob.
- P2: cuando dos reglas aplican, ambas se cargan y la más específica gana en conflictos puntuales (precedencia por subpath).
- P3: el ahorro se mide comparando `input_tokens` al editar un README frente a editar un `.py`.

## Cuándo activar

- Diseñar o auditar la estructura de reglas/memoria de un repo (`CLAUDE.md`, `@rules/*`).
- Decidir si una convención debe ser universal o condicional por glob.
- Reducir el costo de contexto de sesiones que editan archivos de un solo tipo.
- Justificar con números el ahorro de tokens de un esquema condicional por ruta.

## Skills relacionadas

- `katas-custom-commands-skills`
- `katas-session-resume-fork`
- `katas-fewshot-edge-calibration`
