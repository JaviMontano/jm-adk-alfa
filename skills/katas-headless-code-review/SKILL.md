---
name: katas-headless-code-review
version: 1.0.0
description: "Code review headless con claude -p output-format json validado contra schema; el humano sigue siendo gate final de merge."
owner: "JM Labs"
triggers:
  - headless code review
  - claude p json
  - output format json
  - ci annotations
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Katas Headless Code Review

## Qué es

Claude Code corre en CI sin TTY (`claude -p`) y produce JSON estructurado con anotaciones por línea (`file,line,severity,rule_id,message`). El pipeline valida la salida contra un schema declarado y publica comentarios deterministas en el PR. Cero parsing de prosa libre: el modelo anota, el pipeline valida, el humano decide el merge.

## Por qué importa (falla que evita)

Un reviewer humano no escala a 100 PRs/día. Un reviewer LLM en CI encuentra issues consistentes, pero solo si su salida es estructurada. Si se parsea prosa con regex (`grep -E 'ERROR|WARNING'`), el pipeline rompe el primer día que el modelo cambie de redacción o de idioma. La estructura no es cosmética: es la única forma de que la integración sobreviva a la variabilidad del modelo.

## Modelo mental

- `claude -p 'prompt' --output-format=json` produce JSON validable contra un schema declarado, no prosa para humanos.
- El schema es una lista de `Annotation`: `{file, line, severity, rule_id, message}`.
- Si la salida no valida contra el schema, el job **falla** — no se "ajusta" el parser ni se publican comentarios parciales.
- El humano sigue siendo el gate final de merge: el LLM **anota**, no **aprueba**. Puede tener falsos positivos y falsos negativos y no asume responsabilidad legal del merge.
- Combina tres katas: extracción defensiva con schema (Kata 5), control por señal de salida (Kata 1) y el flag `--output-format=json`.

## Patrón correcto

```yaml
# .github/workflows/review.yml
- name: LLM review
  run: |
    claude -p "$REVIEW_PROMPT" \
      --output-format=json \
      --schema annotations.schema.json > out.json
    python scripts/post_annotations.py out.json
```

`post_annotations.py` valida `out.json` contra el schema antes de publicar: si no valida, sale con código distinto de cero y el job falla.

## Anti-patrón

```bash
claude -p "$REVIEW_PROMPT" > review.txt
grep -E 'ERROR|WARNING|issue' review.txt | awk '{...}' | xargs gh pr comment
```

Parsea prosa libre con `grep`/`awk`: se rompe en cuanto el modelo cambie de redacción, idioma o formato. No hay contrato, solo heurística frágil.

## Argumento de certificación

El flag `--output-format=json` fuerza salida estructurada; la validación contra schema declarado es extracción defensiva (Kata 5); el control por señal de salida (Kata 1) decide éxito o fallo del job sin parsear prosa. Si el JSON no valida, el job falla y ningún comentario se publica: un humano investiga. El humano sigue siendo el gate final de merge porque el LLM puede tener FP/FN y no asume responsabilidad del merge.

## Cuándo activar

- Se pide correr code review automatizado en CI/CD con `claude -p`.
- Se necesita salida estructurada (JSON) validada contra schema para publicar anotaciones en un PR.
- Se quiere reemplazar parsing de prosa por un contrato declarado y determinista.
- NO activar para code review interactivo en local sin pipeline, ni cuando el objetivo es aprobar/mergear automáticamente sin humano.

## Skills relacionadas

- `katas-defensive-structured-extraction`
- `katas-mcp-structured-errors`
- `katas-human-handoff-protocol`
