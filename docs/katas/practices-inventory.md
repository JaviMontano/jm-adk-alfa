# Inventario de Prácticas — 30 Katas Claude Certified Architect

> Derivado de [`katas-content.md`](./katas-content.md). Cada práctica es una capacidad arquitectónica verificable.
> **Gap repo** = estado de implementación en JM-ADK antes de este trabajo. Evidencia: PDF `[DOC]` + auditoría de repo `[CÓDIGO]`/`[CONFIG]`.

## Matriz de prácticas

| # | Práctica | Dominio | Escenarios | Gap repo (antes) | Cierre (Fase D/E) |
|--:|----------|---------|-----------|------------------|-------------------|
| 01 | Control de bucle por `stop_reason`, no por prosa | D1 | Support, Multi-Agent | narrativo | skill `katas-deterministic-agent-loop` |
| 02 | Guardarrailes PreToolUse con `permissionDecision:deny` | D1 | Support, Fin.Compliance | **hook solo bloquea regex hardcoded, no política externa** | `pre-tool-guard.sh` policy-driven + guardrails JSON + skill |
| 03 | Normalización PostToolUse vía `updatedMCPToolOutput` | D1 | Support, Legacy ERP | **hook solo loguea** | doc + `posttooluse-normalize` ref + skill |
| 04 | Aislamiento hub-and-spoke (AgentDefinition+Task) | D1 | Multi-Agent, Code Audit | parcial (triada secuencial) | skill `katas-hub-and-spoke-isolation` |
| 05 | Extracción defensiva con JSON Schema + tool_choice | D2 | Struct.Extract, Support | **sin schema semántico** | `references/schemas/` + skill |
| 06 | Errores MCP tipados (isError/errorCategory/isRetryable) | D2 | Support, API Reliability | ausente | skill `katas-mcp-structured-errors` |
| 07 | Exploración segura con Plan Mode (read-only + firma) | D3 | Dev Prod, Code Gen | narrativo | skill + nota hooks plan-mode |
| 08 | Memoria jerárquica CLAUDE.md + @imports | D3 | Dev Prod, Code Gen | presente (2-tier) | skill formaliza precedencia |
| 09 | Reglas condicionales por glob de ruta | D3 | Dev Prod, Code Gen | **solo por IDE, no por ruta** | manifiesto path-rules + skill |
| 10 | Prefix caching (estático-first, dinámico-last) | D5 | Support, Dev Prod | **ausente** | `references/reliability/prefix-caching.md` + skill |
| 11 | Dilución softmax: edge placement + compactación | D5 | Multi-Agent Orch | parcial | `references/reliability/context-dilution.md` + skill |
| 12 | Prompt chaining multi-pass con schemas de transición | D5 | Multi-Agent Orch | presente (fases) | skill formaliza schemas |
| 13 | Code review headless `claude -p --output-format=json` | D1 | CI/CD Automation | **CI parsea, sin schema JSON** | `validate.yml` + `annotations.schema.json` + `post_annotations.py` + skill |
| 14 | Few-shot para calibrar bordes subjetivos | D4 | Struct.Extract | ausente | skill `katas-fewshot-edge-calibration` |
| 15 | Evaluación crítica: cross-check numérico + mismatch flag | D4 | Support, Struct.Extract | ausente | skill `katas-critical-self-correction` |
| 16 | Handoff a humano con payload tipado autocontenido | D1 | Support | parcial (degraded mode) | skill `katas-human-handoff-protocol` |
| 17 | Procesamiento masivo Message Batches API + custom_id | D4 | CI/CD Auto, Struct.Extract | **ausente** | `scripts/batch/batch-runner.py` + skill |
| 18 | Scratchpad persistente curado (sobrevive /compact) | D5 | Developer Prod | presente (tasklog auto) | skill formaliza curado por agente |
| 19 | Investigación adaptativa con budget + re-plan disciplinado | D1 | Multi-Agent Orch, Code Gen | ausente | skill `katas-adaptive-investigation` |
| 20 | Provenance tipada (no claim sin source) + conflict flag | D5 | Multi-Agent, Struct.Extract | presente (evidence tags) | skill formaliza invariante schema |
| 21 | Calidad de descripciones de tools (rename+split) | D2 | Support, Multi-Agent, Dev Prod | parcial | check WARN en `validate-skills.py` + skill |
| 22 | Configuración MCP (project vs user scope, env-var) | D2 | Support, Dev Prod | parcial (1 server) | skill + doc scopes |
| 23 | Selección de built-in tools (Grep→Read→Edit) | D2 | Dev Prod, Code Gen | parcial | skill `katas-builtin-tool-selection` |
| 24 | Slash commands vs skills (context:fork, allowed-tools) | D3 | Code Gen, Dev Prod | presente | skill formaliza criterio |
| 25 | Gestión de sesiones resume vs fork vs fresh | D3 | Support, Code Gen, Dev Prod | presente (registry) | skill formaliza criterio stale |
| 26 | Validación + retry con error feedback específico | D4 | CI/CD, Struct.Extract | ausente | skill `katas-validation-retry-feedback` |
| 27 | Multi-pass review con reviewer independiente | D4 | Code Gen, CI/CD | ausente | skill `katas-independent-reviewer-multipass` |
| 28 | Propagación errores multi-agente estructurada | D1 | Support, Multi-Agent | parcial | skill `katas-multiagent-error-propagation` |
| 29 | Confidence calibration + stratified sampling | D4 | Multi-Agent, Struct.Extract | **thin** | `scripts/qa/run-adversarial-tests.py` ext + skill |
| 30 | Criterios explícitos para reducir falsos positivos | D4 | Support, CI/CD, Struct.Extract | **thin** | skill + criterios categóricos en QA |

## Resumen de cobertura (antes del trabajo)

| Estado | Conteo | Katas |
|--------|-------:|-------|
| Ausente / thin | 9 | 05, 06, 10, 14, 15, 17, 19, 29, 30 |
| Parcial | 9 | 02, 03, 04, 09, 16, 21, 22, 23, 28 |
| Presente (formalizable) | 12 | 01, 07, 08, 11, 12, 13, 18, 20, 24, 25 |

> Las 30 prácticas reciben una skill `katas-*` dedicada (Fase E). 9 prácticas además reciben mejoras sistémicas de infraestructura (Fase D), priorizadas por gap.

## Mecánicas transversales del examen (para todas las skills)

1. **Señal estructurada > prosa** (01, 02, 03, 06, 13, 16, 26, 28): el control vive en campos tipados, nunca en texto del modelo.
2. **Runtime > convención** (02, 03, 04, 07): hooks y SDK garantizan; los autores de tools no.
3. **Aislamiento estructural** (04, 11, 12, 24, 25, 27): sesiones nuevas/forks evitan contaminación de contexto.
4. **Humano como gate final** (13, 15, 16, 20, 29, 30): el LLM anota/propone; el humano decide en lo irreversible.
5. **Economía de contexto** (08, 09, 10, 11, 18): estático-first, condicional por ruta, compactación, scratchpad.
6. **Falla explícita, nunca silenciosa** (01, 06, 15, 20, 26, 28): enmascarar error como éxito vacío es el anti-patrón canónico.
