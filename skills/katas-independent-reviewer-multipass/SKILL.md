---
name: katas-independent-reviewer-multipass
version: 1.0.0
description: "Multi-pass review con reviewer independiente en sesion limpia; per-file y cross-file; rechazo de quorum N-de-M."
owner: "JM Labs"
triggers:
  - independent reviewer
  - multipass review
  - self-review bias
  - per-file cross-file
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Katas Independent Reviewer Multipass

## Qué es

El modelo que generó código retiene el contexto de su propio razonamiento: por eso es un mal revisor de su propio output. Una instancia independiente —una sesión nueva, sin la cadena de generación— ve únicamente el código resultante y detecta más issues reales. Para PRs grandes la revisión se descompone en dos pases: Pass A de profundidad per-file (un deep dive por archivo) y Pass B de integración cross-file (interacciones, duplicados de findings, contratos rotos entre módulos).

## Por qué importa (falla que evita)

El self-review produce reviews superficiales o auto-justificativas: el modelo defiende decisiones que tomó momentos antes, da feedback inconsistente y omite bugs obvios porque su atención sigue anclada a la narrativa de generación. Un single-pass sobre 14 archivos dispersa la atención y diluye los hallazgos. Y "consensuar 2 de 3 reviews" (quorum N-de-M) parece robusto pero suprime issues raros legítimos: un bug que solo un reviewer detecta es descartado por minoría justo cuando más valor aporta.

## Modelo mental

- **Self-review:** misma sesión, contexto sesgado por la generación, ineficaz para detectar fallos propios.
- **Independent reviewer:** sesión limpia, sin la cadena de generación; ve solo el código resultante.
- **Pass A:** per-file deep dive, un archivo a la vez, atención concentrada.
- **Pass B:** cross-file integration, opera solo sobre los resúmenes tipados del Pass A, no sobre el código crudo completo.
- **Quorum 2-de-3 NO es solución:** filtra issues raros legítimos en lugar de compensar el sesgo de contexto.

## Patrón correcto

```python
def review_pr(client, files):
    # Pass A: cada archivo revisado por una SESIÓN NUEVA e independiente.
    per_file = [
        review_file_independent(client, path, content)
        for path, content in files.items()
    ]
    # Pass B: integración cross-file solo sobre los resúmenes tipados.
    summary = json.dumps(per_file)
    return create(
        system="Detecta interacciones cross-file y duplicados de findings.",
        messages=[summary],
    )

# review_file_independent usa una SESIÓN NUEVA: el reviewer NO vio la generación.
```

## Anti-patrón

```python
# ANTI: self-review en la misma sesión que generó el código.
resp_gen = create(messages=[{"role": "user", "content": "Genera el módulo X"}])
# ...misma sesión, contexto sesgado...
create(messages=[resp_gen, {"role": "user", "content": "Ahora revisa lo que escribiste"}])

# ANTI: quorum 2-de-3 que descarta señal genuina.
# si solo 1 de 3 reviewers reporta el bug => se descarta (FALSO NEGATIVO)
```

## Argumento de certificación

- Enunciar por qué el self-review es subóptimo (contexto sesgado de la generación).
- Separar explícitamente el Pass A (per-file) del Pass B (cross-file integration).
- Argumentar contra el quorum N-de-M: filtra señal genuina rara en vez de compensar el sesgo.
- Asegurar sesiones limpias para los reviewers independientes (sin la cadena de generación).

## Cuándo activar

- PRs o changesets grandes (varios archivos) que requieren revisión profunda.
- Pipelines de CI/CD donde el reviewer debe ser independiente del generador.
- Escenarios Code Gen donde el mismo modelo generó y se pediría que revise.
- Cuando alguien propone "consensuar varias reviews por mayoría" y hay que rechazar el quorum.

## Skills relacionadas

- `katas-multipass-prompt-chaining`
- `katas-false-positive-criteria`
- `katas-confidence-stratified-sampling`
