<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-path-conditional-rules
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Path Conditional Rules Body of Knowledge

## Canon

Kata 09 · Reglas condicionales por ruta. Dos clases de reglas conviven en un repo:

- **Universales** (políticas de seguridad): se cargan en TODA edición. Van como import directo en el `CLAUDE.md` raíz, sin glob.
- **Condicionales por glob** (heurísticas de lenguaje: estilo, lints, testing): se cargan solo cuando el agente edita un archivo que matchea el glob declarado (`src/**/*.py`, `*.tf`) y se descartan al salir.

La regla declara su glob de activación. El costo de contexto se paga solo cuando aplica, no en cada sesión.

### Conceptos clave

- **Glob de activación:** patrón de ruta que enciende una regla (`src/**/*.py`, `*.tf`).
- **Regla universal:** sin glob, siempre cargada (seguridad).
- **Carga / descarga por archivo:** la regla entra al contexto al tocar un archivo que matchea y sale al salir.
- **Precedencia por subpath:** si dos reglas aplican, ambas cargan y la más específica gana en conflictos puntuales.
- **Ahorro medible:** comparar `input_tokens` editando un README contra editar un `.py`.

## Quality Signals

| Signal | Target |
|---|---|
| Clasificación explícita | Cada regla está marcada como universal o condicional por glob |
| Cobertura de seguridad | Las políticas de seguridad son universales, nunca escondidas tras un glob |
| Globs sin huecos | Los globs cubren los tipos de archivo relevantes sin solapes ambiguos |
| Ahorro medible | El beneficio se cuantifica con `input_tokens` README vs `.py` |
| Update safety | Overrides locales preservados; cambios aditivos |

## Anti-patrón canónico

Un `CLAUDE.md` monolítico que importa todas las reglas (Python + Terraform + Go + Testing + Security) y las carga en cada sesión, pagando 2000 líneas de contexto incluso al editar un README. El remedio es separar las heurísticas de lenguaje en bloques `## When editing <glob>:` y dejar solo lo universal en carga directa.

## Open Knowledge

- Añadir referencias específicas del proyecto a medida que se estabilicen los globs reales del repo.
