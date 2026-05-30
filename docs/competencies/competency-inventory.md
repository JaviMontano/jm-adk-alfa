# Inventario de Competencias — 22 skills de capacidad construible

> Las `katas-*` entrenan para el examen; estas competencias **construyen** la capacidad en producción.
> Nombre directo (sin prefijo). Fuente: [`competency-content.md`](./competency-content.md). Scaffold: `scripts/scaffold-competencies.sh`.

| slug | capacidad | katas que agrega |
|------|-----------|------------------|
| `hook-engineering` | Hooks deterministas PreToolUse/PostToolUse | 02, 03, 07 |
| `agentic-loop-engineering` | Bucle por señal estructurada + budget | 01 |
| `subagent-orchestration` | Hub-and-spoke + propagación de errores | 04, 28 |
| `structured-output-design` | JSON Schema defensivo + tool_choice | 05 |
| `mcp-engineering` | MCP config + contratos de error | 06, 22 |
| `tool-use-design` | Descripciones contrato + built-in strategy | 21, 23 |
| `plan-mode-workflow` | Exploración segura dos modos | 07 |
| `claude-md-architecture` | Memoria jerárquica + reglas por ruta | 08, 09 |
| `context-window-engineering` | Prefix caching + dilución | 10, 11 |
| `prompt-chaining-design` | Multi-pass + schemas de transición | 12 |
| `few-shot-engineering` | Few-shot de bordes cache-friendly | 14 |
| `self-correction-loops` | Verificación cruzada + mismatch | 15 |
| `human-escalation-design` | Handoff tipado end-state | 16 |
| `message-batch-orchestration` | Batches offline + custom_id | 17 |
| `persistent-memory-design` | Scratchpad persistente | 18 |
| `adaptive-investigation-method` | Investigación con budget + re-plan | 19 |
| `provenance-engineering` | Provenance tipada + conflictos | 20 |
| `custom-tooling-extension` | Commands + skills (fork, allowed-tools) | 24 |
| `session-lifecycle-management` | Resume / fork / fresh | 25 |
| `validation-retry-design` | Retry con error feedback | 26 |
| `independent-review-design` | Reviewer independiente per/cross-file | 27 |
| `evaluation-confidence-design` | Calibración + falsos positivos | 29, 30 |

Contrato CI idéntico a las `katas-*` (16 archivos, frontmatter, JSON válido, sin links relativos rotos).
