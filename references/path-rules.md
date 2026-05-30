# Reglas Condicionales por Ruta (Kata 09)

> Manifiesto de reglas por glob para JM-ADK. Las reglas universales se cargan siempre; las heurísticas por lenguaje/área se cargan **solo** cuando el agente edita archivos que matchean su glob — liberando contexto (Kata 10/11) para el resto.

## Modelo

- Cada regla declara su **glob de activación**.
- El agente carga la regla al entrar a un archivo que matchea, la descarta al salir.
- Reglas grandes (heurísticas de lenguaje) → **condicionales**.
- Reglas universales (políticas de seguridad) → **siempre cargadas**.
- En conflicto puntual, la regla más específica por subpath gana (precedencia, Kata 08).

## Manifiesto

| Glob de activación | Regla a cargar | Tipo |
|--------------------|----------------|------|
| `**/*` (siempre) | `references/guardrails/tool-policy.json` (seguridad, Kata 02) | universal |
| `**/*` (siempre) | Constitution (gates G0–G3) | universal |
| `scripts/**/*.py`, `**/*.py` | PEP8 + type hints + stdlib-first (ver `.specify/CONSTITUTION.md`) | condicional |
| `scripts/**/*.sh`, `**/*.sh` | shellcheck `-S error` clean; quoting estricto; sin `set -e` frágil | condicional |
| `skills/**/SKILL.md` | contrato de 16 archivos + frontmatter `name/version/description` | condicional |
| `**/*.json` | debe parsear (`python3 -m json.tool`); sin secretos literales | universal (validación) |
| `.github/workflows/**/*.yml` | pasos idempotentes; sin secretos inline; CI-safe | condicional |
| `docs/**/*.md` | prosa ES + identificadores EN; sin links relativos rotos | condicional |

## Por qué condicional y no monolítico

Un `CLAUDE.md` que carga 2000 líneas para todos los archivos paga el costo en todas las sesiones, incluso cuando el agente solo edita un README. Cargar reglas Python solo al tocar `*.py` libera contexto para el resto. La verificación empírica es medir `input_tokens` editando un README vs editando un `.py`.

## Anti-patrón

`CLAUDE.md` monolítico con Python+Terraform+Go+Testing+Security cargando siempre, aunque solo edites un README → atención dispersa (Kata 11), caché caro (Kata 10), y cambiar una regla afecta sesiones que nada tienen que ver.

Relacionado: `katas-path-conditional-rules`, `katas-hierarchical-claude-memory`, `katas-pretooluse-guardrails`.
