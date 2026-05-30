---
name: katas-tool-description-quality
version: 1.0.0
description: "Calidad de descripciones de tools como contrato de seleccion; rename y split sobre overloading para evitar misroute."
owner: "JM Labs"
triggers:
  - tool description quality
  - tool routing ambiguity
  - rename split tools
  - tool contract
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Katas Tool Description Quality

## Qué es

La descripción de un tool es el único mecanismo que el modelo usa para escoger entre tools similares. Una buena descripción no es prosa decorativa: es un contrato de uso que declara tres cosas concretas: el **input format** que acepta, **ejemplos de query** que la disparan, y la **frontera explícita** ("usa esto en lugar de X cuando..."). El nombre del tool es parte del contrato; cuando el nombre confunde, ninguna cantidad de explicación lo arregla.

Aplica a tres escenarios: Customer Support (enrutamiento entre tools de respuesta), Multi-Agent (selección entre agentes con capacidades solapadas) y Dev Productivity (tools de análisis y extracción que compiten por el mismo turno).

## Por qué importa (falla que evita)

Cuando dos tools tienen descripciones genéricas (`Analyzes content` vs `Analyzes documents`), el modelo enruta mal en 20–30% de los turnos. El síntoma es traicionero: una "respuesta razonable pero del tool incorrecto", que pasa desapercibida en los logs hasta que un componente downstream rompe porque recibió el shape equivocado. No es un crash visible; es deriva silenciosa de routing que se acumula.

## Modelo mental

- **Descripción = contrato de uso.** Contratos solapados son ambiguos por diseño; el modelo no puede desempatar lo que tú no desambiguaste.
- **Renombrar suele superar a "explicar más"** cuando el nombre confunde: `analyze_content` → `extract_web_results` resuelve más misroutes que tres párrafos extra.
- **Splitting beats overloading:** cinco tools con un propósito único son mejores que uno con cinco modos. Un tool multimodo obliga al modelo a inferir el modo además del tool.
- **El system prompt interactúa con la descripción:** ciertas keywords en el prompt pueden sesgar el routing hacia un tool aunque el contenido pida otro.
- La frontera debe ser **recíproca:** si A dice "para PDF usa B", B debe decir "para HTML usa A".

## Patrón correcto

```json
{
  "name": "extract_web_results",
  "description": "Parses HTML pages from a search query into a list of {title,url,snippet}. Use when input is a URL or raw HTML; for PDF/DOCX use parse_document instead."
}
```

Con su par recíproco `parse_document`, cuya descripción declara el input format inverso y devuelve la frontera ("para HTML o URLs usa `extract_web_results`").

## Anti-patrón

```json
[
  {"name":"analyze_content","description":"Analyzes content"},
  {"name":"analyze_document","description":"Analyzes documents"}
]
```

Dos contratos genéricos y solapados, sin input format, sin frontera, sin ejemplo de query. El modelo adivina y acierta el 70–80% de las veces.

## Argumento de certificación

Para certificar dominio de esta kata hay que sostener cuatro afirmaciones:

1. La descripción es el árbitro de selección entre tools; el modelo no ve la implementación.
2. Saber identificar tools ambiguos por contrato solapado (mismo verbo, sustantivos casi sinónimos, cero frontera).
3. Proponer **rename + split** antes que "explicar más" cuando el nombre es la fuente de confusión.
4. Detectar keywords del system prompt que sesgan el routing y neutralizarlas enunciando la frontera explícitamente en la descripción.

## Cuándo activar

- Hay dos o más tools que el modelo confunde y se observan respuestas correctas pero del tool equivocado.
- Se diseña una toolset nueva y se quiere prevenir misroute por contrato solapado.
- Un tool acumula modos (overloading) y conviene evaluar split.
- El system prompt menciona keywords que sesgan el routing hacia el tool equivocado.

## Skills relacionadas

- `katas-mcp-server-configuration`
- `katas-builtin-tool-selection`
- `katas-custom-commands-skills`
