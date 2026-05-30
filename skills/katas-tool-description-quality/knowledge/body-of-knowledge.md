<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-tool-description-quality
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Tool Description Quality Body of Knowledge

## Canon

La descripción de un tool es el único mecanismo de selección que el modelo usa entre tools similares. Es un contrato de uso con tres componentes obligatorios:

1. **Input format** — qué shape acepta (URL, raw HTML, PDF, DOCX...).
2. **Ejemplos de query** — qué disparadores la activan.
3. **Frontera explícita** — "usa esto en lugar de X cuando...", y debe ser recíproca entre los tools que compiten.

### Conceptos clave

- **Contrato de selección.** El modelo no ve la implementación; elige por `name` + `description` + `input_schema`. Contratos solapados son ambiguos por diseño.
- **Rename sobre "explicar más".** Cuando el nombre confunde, renombrar (`analyze_content` → `extract_web_results`) supera a añadir párrafos.
- **Split sobre overloading.** Cinco tools con un propósito único > uno con cinco modos; el split elimina la inferencia de modo.
- **Interacción con el system prompt.** Keywords del prompt sesgan el routing; la frontera explícita en la descripción contrarresta el sesgo.

## Quality Signals

| Signal | Target |
|---|---|
| Input format declarado | Cada descripción dice qué shape acepta |
| Ejemplo de query | La descripción incluye al menos un disparador concreto |
| Frontera recíproca | Cada tool dice cuándo usar el otro, y el otro lo confirma |
| Nombre no confunde | El `name` describe el propósito, no un verbo genérico |
| Misroute observado | <5% en evals; el síntoma es "tool incorrecto, respuesta razonable" |

## Anti-patrón canónico

```json
[
  {"name":"analyze_content","description":"Analyzes content"},
  {"name":"analyze_document","description":"Analyzes documents"}
]
```

Dos verbos idénticos, sustantivos casi sinónimos, cero input format, cero frontera. Produce misroute en 20–30% de los turnos, invisible en logs hasta que un downstream rompe por recibir el shape equivocado.

## Open Knowledge

- Medir la tasa de misroute con un eval set de queries límite (HTML vs PDF, compliance interno vs externo).
- Documentar las keywords del system prompt que históricamente sesgaron el routing en cada proyecto.
