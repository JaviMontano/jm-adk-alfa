# Competency Content — Capacidades de Ingeniería Agéntica (fuente canónica)

> Las skills `katas-*` son **entrenamiento** (práctica del examen Claude Certified Architect).
> Estas competencias son la **capacidad construible subyacente**: cómo se diseña, implementa y valida cada capacidad en producción.
> Fuente: derivadas de `docs/katas/katas-content.md` (cada competencia agrega varias katas). Prosa ES, código EN.

## Índice (22 competencias → katas que agregan)

| slug | competencia | katas |
|------|-------------|-------|
| `hook-engineering` | Hooks deterministas (PreToolUse/PostToolUse) | 02, 03, 07 |
| `agentic-loop-engineering` | Bucle agéntico por señal estructurada | 01 |
| `subagent-orchestration` | Orquestación hub-and-spoke + propagación de errores | 04, 28 |
| `structured-output-design` | Salida estructurada con JSON Schema | 05 |
| `mcp-engineering` | MCP: config de servers + contratos de error | 06, 22 |
| `tool-use-design` | Diseño de tools: descripciones + selección built-in | 21, 23 |
| `plan-mode-workflow` | Exploración segura en dos modos | 07 |
| `claude-md-architecture` | Memoria jerárquica + reglas por ruta | 08, 09 |
| `context-window-engineering` | Prefix caching + mitigación de dilución | 10, 11 |
| `prompt-chaining-design` | Encadenamiento multi-pass | 12 |
| `few-shot-engineering` | Few-shot para calibrar bordes | 14 |
| `self-correction-loops` | Verificación cruzada + auto-corrección | 15 |
| `human-escalation-design` | Handoff tipado a humano | 16 |
| `message-batch-orchestration` | Procesamiento masivo offline | 17 |
| `persistent-memory-design` | Scratchpad persistente | 18 |
| `adaptive-investigation-method` | Investigación adaptativa con budget | 19 |
| `provenance-engineering` | Provenance tipada + conflictos | 20 |
| `custom-tooling-extension` | Slash commands + skills | 24 |
| `session-lifecycle-management` | Resume / fork / fresh | 25 |
| `validation-retry-design` | Retry con error feedback | 26 |
| `independent-review-design` | Multi-pass + reviewer independiente | 27 |
| `evaluation-confidence-design` | Confidence calibration + falsos positivos | 29, 30 |

> El review headless (kata 13) y batches (17) se construyen combinando `structured-output-design` + `mcp-engineering` + `message-batch-orchestration`; se referencian, no duplican.

---

## hook-engineering — Hooks deterministas (PreToolUse/PostToolUse)
- **Capacidad:** registrar hooks en `ClaudeAgentOptions.hooks` que el runtime garantiza, para hacer cumplir políticas y normalizar I/O sin depender del modelo.
- **Cuándo:** límites críticos (monetarios, paths, dominios), normalización de outputs heterogéneos, enforcement de modo (plan/write).
- **Cómo construir:** (1) define política en código recargable (dict/JSON), no en prompt. (2) PreToolUse inspecciona `tool_name`+`tool_input` → `permissionDecision: allow|deny|ask` ANTES de ejecutar (cero side-effects). (3) PostToolUse reescribe `tool_response` → `updatedMCPToolOutput` ANTES de entrar al historial. (4) usa `HookMatcher(matcher="*")` o por-tool.
- **GOOD:** deny estructurado desde política hot-reload (ver `references/guardrails/tool-policy.json` + `scripts/pre-tool-guard.sh`).
- **ANTI:** política solo en system prompt (prompt injection la rompe); normalización por-tool (un handler nuevo la olvida).
- **Checklist de validación:** ¿la política vive en código? ¿deny ocurre antes del side-effect? ¿el modelo nunca ve el payload crudo? ¿es auditable?
- **Katas:** 02, 03, 07. **Skills relacionadas:** `katas-pretooluse-guardrails`, `katas-posttooluse-normalization`.

## agentic-loop-engineering — Bucle agéntico por señal estructurada
- **Capacidad:** construir el loop de control que enruta por `stop_reason` tipado, con budget duro y handlers explícitos.
- **Cómo:** `while True`: `tool_use`→dispatch+reinyecta `tool_result` como user; `end_turn`→halt; otro→`raise UnhandledStop`. Budget: `max_iterations`/`BudgetExceeded`.
- **ANTI:** parsear prosa (`"done" in text`) → halt silencioso o bucle infinito.
- **Checklist:** ¿control en `stop_reason`, no en texto? ¿budget configurable? ¿fallos fuertes, no silenciosos?
- **Katas:** 01. **Relacionadas:** `katas-deterministic-agent-loop`.

## subagent-orchestration — Hub-and-spoke + propagación de errores
- **Capacidad:** diseñar coordinadores que despachan subagentes aislados (`AgentDefinition`+Task) y agregan resultados con errores estructurados.
- **Cómo:** cada subagente = sesión nueva, contexto vacío, tools/modelo propios (haiku barato para extracción). Coordinador recibe solo el último mensaje. Errores: `failure_type, attempted_query, partial_results, suggested_alternatives`; local recovery primero; access failure != valid empty; coverage gap annotation; nunca enmascarar error como success vacío.
- **ANTI:** un agente con todo concatenado; `except: return {results:[]}`.
- **Checklist:** ¿aislamiento estructural? ¿blast radius acotado? ¿errores distinguen access-failure de empty? ¿coverage gap explícito?
- **Katas:** 04, 28. **Relacionadas:** `katas-hub-and-spoke-isolation`, `katas-multiagent-error-propagation`.

## structured-output-design — Salida estructurada con JSON Schema
- **Capacidad:** forzar `tool_choice` con schema defensivo: `required` reales, nullable union para opcionales, enums con válvula `'other'`+`details`.
- **ANTI:** "devuelve JSON" en prosa + `json.loads(text)`.
- **Checklist:** ¿required = presente en la fuente? ¿default `''` eliminado (null/unclear)? ¿enums con escape? ¿tool_choice forzado solo cuando no hay decisión de tool?
- **Katas:** 05. **Relacionadas:** `katas-defensive-structured-extraction`, `katas-headless-code-review`.

## mcp-engineering — Config de servers + contratos de error
- **Capacidad:** configurar MCP servers (project vs user scope, env-var expansion) y diseñar errores tipados (`isError, errorCategory, isRetryable, retryAfterSeconds`).
- **Cómo:** `.mcp.json` versionado para equipo, `~/.claude.json` para personal; credenciales `${ENV}` nunca literal; retry policy en el cliente, no en el modelo; secreto leakeado → rotar + purgar history (filter-repo), no gitignore.
- **ANTI:** token literal en archivo versionado; error string genérico que el modelo debe adivinar.
- **Checklist:** ¿scope correcto? ¿credenciales por env-var? ¿error con categoría+retryable? ¿MCP solo cuando un built-in no aplica?
- **Katas:** 06, 22. **Relacionadas:** `katas-mcp-structured-errors`, `katas-mcp-server-configuration`.

## tool-use-design — Descripciones + selección built-in
- **Capacidad:** escribir descripciones de tools como contrato de routing (input format, ejemplos, frontera) y aplicar la estrategia Grep→Read→Edit.
- **Cómo:** rename + split sobre overloading; describir failure mode de Edit (anchor no único) + fallback Read+Write; nunca Read masivo upfront.
- **ANTI:** descripciones genéricas ('Analyzes content'); `glob("**/*")` + read all (200k tokens).
- **Checklist:** ¿descripciones con frontera recíproca? ¿tool correcto por decisión rápida? ¿sin Read masivo?
- **Katas:** 21, 23. **Relacionadas:** `katas-tool-description-quality`, `katas-builtin-tool-selection`.

## plan-mode-workflow — Exploración segura en dos modos
- **Capacidad:** operar repos desconocidos en Plan Mode read-only con `plan.md` firmado antes de escribir; hooks aplican el modo.
- **ANTI:** `bypassPermissions` + write desde el inicio.
- **Checklist:** ¿escritura deshabilitada en plan? ¿aprobación = artefacto auditable? ¿cambios al plan re-piden firma? ¿hook enumera tools de escritura?
- **Katas:** 07. **Relacionadas:** `katas-plan-mode-exploration`.

## claude-md-architecture — Memoria jerárquica + reglas por ruta
- **Capacidad:** estructurar CLAUDE.md user/team/module con `@imports` y reglas condicionales por glob; universales siempre, heurísticas on-demand.
- **ANTI:** monolítico 2000 líneas cargando siempre; preferencias personales en el repo.
- **Checklist:** ¿separación user/team/module? ¿@imports caché-friendly? ¿reglas por glob? ¿precedencia por subpath?
- **Katas:** 08, 09. **Relacionadas:** `katas-hierarchical-claude-memory`, `katas-path-conditional-rules`.

## context-window-engineering — Prefix caching + dilución
- **Capacidad:** organizar contexto estático-first/dinámico-last (cache KV ~10x) y mitigar la curva U (edge placement + compactación >55%).
- **ANTI:** timestamp al inicio (invalida cache); regla crítica enterrada en el centro.
- **Checklist:** ¿prefijo estable sin valores por-turno? ¿`<reminder>` dinámico al final? ¿reglas críticas en bordes? ¿umbral de compactación fijado?
- **Katas:** 10, 11. **Relacionadas:** `katas-prefix-caching`, `katas-context-dilution-mitigation`.

## prompt-chaining-design — Encadenamiento multi-pass
- **Capacidad:** descomponer tareas grandes en pase local tipado + pase de integración que solo ve resúmenes; schemas de transición.
- **ANTI:** mega-prompt concatenando 50 archivos (satura atención, no paraleliza).
- **Checklist:** ¿pase 2 nunca ve crudos? ¿schema por pase? ¿estado de error tipado por unidad? ¿se justifica vs single-pass?
- **Katas:** 12. **Relacionadas:** `katas-multipass-prompt-chaining`.

## few-shot-engineering — Few-shot para calibrar bordes
- **Capacidad:** 2–4 ejemplos del mismo schema que cubren bordes, no centro; al inicio (zona estática, cache-friendly).
- **ANTI:** párrafo abstracto de criterio; >5 ejemplos (dispersa atención, rompe cache).
- **Checklist:** ¿ejemplos = schema de salida? ¿cubren bordes? ¿2–4? ¿al inicio? ¿complementan schema, no lo contradicen?
- **Katas:** 14. **Relacionadas:** `katas-fewshot-edge-calibration`.

## self-correction-loops — Verificación cruzada + auto-corrección
- **Capacidad:** cruzar declarado vs calculado; si difieren > epsilon, `mismatch=true` con ambos valores + escalar; nunca corregir en silencio.
- **ANTI:** confiar en lo declarado; `total=computed` silencioso.
- **Checklist:** ¿campos numéricos identificados? ¿epsilon justificado (cero enteros, pequeño monedas)? ¿mismatch escala a humano?
- **Katas:** 15. **Relacionadas:** `katas-critical-self-correction`.

## human-escalation-design — Handoff tipado a humano
- **Capacidad:** end-state del bucle que invoca `escalate_to_human` con payload autocontenido (`customer_id, issue_summary, actions_taken, escalation_reason, recommended_action`).
- **ANTI:** prosa "voy a hablar con mi supervisor" + sigue generando.
- **Checklist:** ¿precondiciones enumeradas (límite/irreversible/conflicto)? ¿payload autocontenido (humano no lee la conversación)? ¿corta generación?
- **Katas:** 16. **Relacionadas:** `katas-human-handoff-protocol`.

## message-batch-orchestration — Procesamiento masivo offline
- **Capacidad:** Message Batches API para cargas offline (~50% costo); `custom_id` único por request; fragmentación selectiva de fallos.
- **Cómo:** `create → poll processing_status → results`; reintentar solo los failed por custom_id.
- **ANTI:** for síncrono real-time sin custom_id (rompe rate limits, sin fail-isolation).
- **Checklist:** ¿carga es offline/latency-tolerant? ¿custom_id único? ¿reintento selectivo? Ver `scripts/batch/batch-runner.py`.
- **Katas:** 17. **Relacionadas:** `katas-message-batch-processing`.

## persistent-memory-design — Scratchpad persistente
- **Capacidad:** archivo en disco con conclusiones validadas (Hipótesis/Decisiones/Hallazgos/Pendientes) que sobrevive a /compact; leído una vez, referenciado después.
- **ANTI:** memoria en la conversación; scratchpad sin estructura o re-leído cada turno (rompe cache).
- **Checklist:** ¿solo conclusiones validadas? ¿estructurado? ¿lectura única + referencia? ¿sobrevive reset?
- **Katas:** 18. **Relacionadas:** `katas-persistent-scratchpad`.

## adaptive-investigation-method — Investigación adaptativa con budget
- **Capacidad:** mapeo barato → priorización → deep-dive selectivo; re-plan solo al invalidar hipótesis; budget duro.
- **ANTI:** plan rígido upfront; `read_all_files()`; re-plan reflejo cada turno.
- **Checklist:** ¿budget de exploración? ¿criterio de re-plan explícito? ¿persiste plan+findings en scratchpad?
- **Katas:** 19. **Relacionadas:** `katas-adaptive-investigation`.

## provenance-engineering — Provenance tipada + conflictos
- **Capacidad:** invariante 'no hay claim sin source'; conflictos `conflict=true` con ambas fuentes, escalados, no promediados.
- **ANTI:** resumen en prosa sin source_id ni fecha ni conflicto.
- **Checklist:** ¿cada claim con source[]? ¿conflictos marcados, no resueltos? ¿fecha visible para el humano? ¿test estructural de provenance?
- **Katas:** 20. **Relacionadas:** `katas-provenance-preservation`.

## custom-tooling-extension — Slash commands + skills
- **Capacidad:** extender Claude Code con commands (`.claude/commands/X.md`) y skills (`context: fork`, `allowed-tools`, `argument-hint`); scope project vs user.
- **ANTI:** user scope (no replica); skill sin fork (contamina sesión) ni allowed-tools (destructive ops).
- **Checklist:** ¿command vs skill por trigger/scope? ¿fork para economía de contexto? ¿allowed-tools whitelist? ¿convenciones permanentes en CLAUDE.md, no en skill?
- **Katas:** 24. **Relacionadas:** `katas-custom-commands-skills`.

## session-lifecycle-management — Resume / fork / fresh
- **Capacidad:** decidir resume (contexto válido) vs fork (ramas paralelas) vs fresh+summary (mundo cambió, tool results stale).
- **ANTI:** resume tras refactor masivo; pegar transcript completo viejo.
- **Checklist:** ¿tool results stale detectados? ¿summary tipado del scratchpad? ¿forks sin interferencia?
- **Katas:** 25. **Relacionadas:** `katas-session-resume-fork`.

## validation-retry-design — Retry con error feedback
- **Capacidad:** loop extract→validate→retry-with-error-feedback específico; recuperable (formato) vs no recuperable (dato ausente); max 2–3; luego escalar con cadena de errores.
- **ANTI:** retry sin feedback (mismo prompt); aceptar salida fallida en silencio.
- **Checklist:** ¿feedback = error específico? ¿distingue recuperable? ¿detecta patrón sistemático para fix estructural? ¿escala al agotar retries?
- **Katas:** 26. **Relacionadas:** `katas-validation-retry-feedback`.

## independent-review-design — Multi-pass + reviewer independiente
- **Capacidad:** reviewer en sesión limpia (no vio la generación); per-file + cross-file pass; sin quorum N-de-M (filtra señal rara).
- **ANTI:** self-review en misma sesión; quorum 2-de-3.
- **Checklist:** ¿reviewer independiente? ¿per-file y cross-file separados? ¿sin quorum que suprima issues legítimos?
- **Katas:** 27. **Relacionadas:** `katas-independent-reviewer-multipass`.

## evaluation-confidence-design — Calibración + falsos positivos
- **Capacidad:** calibrar confidence contra labeled set; stratified sampling por document_type; criterios categóricos con ejemplos +/- por severidad; disable temporal de categoría con alto FP; accuracy desglosada.
- **ANTI:** confiar en confidence raw; 'be conservative' vago; accuracy agregada.
- **Checklist:** ¿confidence calibrada (no raw)? ¿muestreo estratificado? ¿criterios categóricos con +/-? ¿FP rate por categoría? Ver `scripts/qa/run-confidence-fp-tests.py`.
- **Katas:** 29, 30. **Relacionadas:** `katas-confidence-stratified-sampling`, `katas-false-positive-criteria`.
