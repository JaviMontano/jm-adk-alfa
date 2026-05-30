<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-headless-code-review
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Headless Code Review Body of Knowledge

## Canon

Code review headless en CI/CD: Claude Code corre sin TTY (`claude -p`) y emite JSON estructurado, no prosa. El pipeline valida ese JSON contra un schema declarado y publica anotaciones deterministas en el PR. El LLM anota; el humano sigue siendo el gate final de merge.

## Conceptos clave

- **Modo headless (`claude -p`):** invocación no interactiva, apta para runners de CI sin terminal.
- **`--output-format=json`:** fuerza salida estructurada validable, no texto para humanos.
- **Schema de anotaciones:** lista de `Annotation` = `{file, line, severity, rule_id, message}`. `severity` es un enum; los campos son `required` reales (extracción defensiva, Kata 5).
- **Validación dura (control por señal, Kata 1):** si la salida no valida contra el schema, el job falla; no se "ajusta" el parser ni se publican comentarios parciales.
- **Gate humano:** el LLM anota, no aprueba. Puede tener FP/FN y no asume responsabilidad legal del merge.

## Señales de calidad

| Señal | Objetivo |
|---|---|
| Salida estructurada | `--output-format=json` presente; nunca se parsea prosa |
| Validación contra schema | `out.json` valida contra `annotations.schema.json` o el job falla |
| Determinismo de publicación | Comentarios derivan del JSON validado, no de regex sobre texto |
| Gate de merge | Humano decide el merge; el agente solo anota |

## Anti-patrón canónico

```bash
claude -p "$REVIEW_PROMPT" > review.txt
grep -E 'ERROR|WARNING|issue' review.txt | awk '{...}' | xargs gh pr comment
```

Parsea prosa libre con `grep`/`awk`: se rompe el primer día que el modelo cambie de redacción o idioma. Sin contrato estructurado, la integración es frágil por diseño.

## Quiz canónico

- Respuestas: B · C · B.
- P2: si el JSON no valida, el job falla y no se publican comentarios; el humano investiga.
- P3: el LLM puede tener FP/FN y no asume responsabilidad legal del merge, por eso el humano es gate final.
