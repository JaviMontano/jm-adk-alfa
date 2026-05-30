# Inventario de Skills `katas-*` — 30 skills (1 por kata)

> Spec de scaffolding para Fase E. Cada fila es un `python3 scripts/scaffold-skill.py --name <slug> --description "<desc>" --triggers "<t>" --allowed-tools "Read,Grep,Glob,Bash" --apply`.
> Triggers son multi-palabra (evitan colisión con HIGH_RISK_TRIGGERS de `validate-skills.py`). Owner `JM Labs`, version `1.0.0`.
> Convención de contenido: prosa ES + código EN. Fuente: [`katas-content.md`](./katas-content.md).

## Tabla de skills

| # | slug | description (resumen) | triggers | dominio |
|--:|------|----------------------|----------|---------|
| 01 | `katas-deterministic-agent-loop` | Control de bucle agéntico por stop_reason tipado, no por prosa del modelo. | `deterministic loop, stop_reason, agent loop control, budget exceeded` | D1 |
| 02 | `katas-pretooluse-guardrails` | Guardarrailes deterministas en hook PreToolUse con permissionDecision deny desde política recargable. | `pretooluse guardrail, permission decision, policy gate, deterministic guardrail` | D1 |
| 03 | `katas-posttooluse-normalization` | Normalización de outputs heterogéneos vía hook PostToolUse y updatedMCPToolOutput. | `posttooluse normalization, output normalization, updatedmcptooloutput, legacy payload` | D1 |
| 04 | `katas-hub-and-spoke-isolation` | Aislamiento multi-agente con AgentDefinition + built-in Task, contexto vacío por subagente. | `hub and spoke, subagent isolation, agentdefinition, task tool isolation` | D1 |
| 05 | `katas-defensive-structured-extraction` | Extracción defensiva con JSON Schema, tool_choice forzado, enums con escape y nullable explícito. | `defensive extraction, json schema extraction, tool_choice forced, nullable union` | D2 |
| 06 | `katas-mcp-structured-errors` | Errores MCP tipados (isError, errorCategory, isRetryable, retryAfterSeconds) para decisión del cliente. | `mcp structured error, error category, retryable error, typed error contract` | D2 |
| 07 | `katas-plan-mode-exploration` | Exploración segura en Plan Mode read-only con plan.md firmado por humano antes de escritura. | `plan mode, read-only exploration, plan approval, safe exploration` | D3 |
| 08 | `katas-hierarchical-claude-memory` | Memoria jerárquica CLAUDE.md user/team/module con @imports y precedencia por especificidad. | `hierarchical memory, claude md memory, memory imports, memory precedence` | D3 |
| 09 | `katas-path-conditional-rules` | Reglas condicionales por glob de ruta; universales siempre, heurísticas on-demand. | `path conditional rules, glob rules, conditional memory, per-path rules` | D3 |
| 10 | `katas-prefix-caching` | Prefix caching: estático-first, dinámico-last; interpretar cache_creation vs cache_read tokens. | `prefix caching, kv cache, cache control, static prefix` | D5 |
| 11 | `katas-context-dilution-mitigation` | Mitigación de dilución softmax: edge placement de reglas críticas + compactación a 50-60%. | `context dilution, lost in the middle, edge placement, context compaction` | D5 |
| 12 | `katas-multipass-prompt-chaining` | Prompt chaining multi-pass: pase local tipado + pase de integración sobre resúmenes. | `prompt chaining, multipass chaining, local then integrate, chaining schema` | D5 |
| 13 | `katas-headless-code-review` | Code review headless con claude -p --output-format=json validado contra schema; humano gate final. | `headless code review, claude -p json, output-format json, ci annotations` | D1 |
| 14 | `katas-fewshot-edge-calibration` | Few-shot para calibrar bordes subjetivos; 2-4 ejemplos del mismo schema. | `few-shot calibration, edge examples, fewshot prompting, subjective calibration` | D4 |
| 15 | `katas-critical-self-correction` | Evaluación crítica: cross-check numérico declarado vs calculado, mismatch flag, sin corregir en silencio. | `critical self-correction, numeric cross-check, mismatch flag, computed vs stated` | D4 |
| 16 | `katas-human-handoff-protocol` | Handoff a humano con payload tipado autocontenido; end-state del bucle, no pausa. | `human handoff, escalate to human, handoff payload, escalation protocol` | D1 |
| 17 | `katas-message-batch-processing` | Procesamiento masivo con Message Batches API, custom_id por request, fragmentación selectiva. | `message batches, batch processing, custom_id, offline batch` | D4 |
| 18 | `katas-persistent-scratchpad` | Scratchpad persistente en disco curado por el agente; sobrevive /compact y reinicios. | `persistent scratchpad, investigation scratchpad, durable memory, scratchpad file` | D5 |
| 19 | `katas-adaptive-investigation` | Investigación adaptativa: mapeo barato, budget acotado, re-plan disciplinado al invalidar hipótesis. | `adaptive investigation, dynamic decomposition, exploration budget, re-plan discipline` | D1 |
| 20 | `katas-provenance-preservation` | Provenance tipada: no claim sin source; conflictos marcados y escalados, no promediados. | `provenance preservation, claim source mapping, conflict flag, source provenance` | D5 |
| 21 | `katas-tool-description-quality` | Calidad de descripciones de tools: input format, ejemplos, frontera; rename + split sobre overload. | `tool description quality, tool routing ambiguity, rename split tools, tool contract` | D2 |
| 22 | `katas-mcp-server-configuration` | Configuración MCP: project vs user scope, env-var expansion, rotación ante secreto leakeado. | `mcp server configuration, mcp scope, env var credentials, mcp json config` | D2 |
| 23 | `katas-builtin-tool-selection` | Selección de built-in tools: Grep→Read→Edit, failure modes, sin Read masivo upfront. | `builtin tool selection, grep read edit, tool strategy, edit anchor` | D2 |
| 24 | `katas-custom-commands-skills` | Slash commands vs skills: context fork, allowed-tools whitelist, argument-hint, scope project/user. | `custom slash commands, skills frontmatter, context fork skill, command vs skill` | D3 |
| 25 | `katas-session-resume-fork` | Gestión de sesiones: resume vs fork vs fresh con summary; detectar tool results stale. | `session resume, session fork, fresh summary session, stale tool results` | D3 |
| 26 | `katas-validation-retry-feedback` | Validación + retry con error feedback específico; recuperable vs no recuperable; max 2-3 intentos. | `validation retry, error feedback loop, retry with feedback, recoverable error` | D4 |
| 27 | `katas-independent-reviewer-multipass` | Multi-pass review con reviewer independiente (sesión limpia); per-file + cross-file; sin quorum. | `independent reviewer, multipass review, self-review bias, per-file cross-file` | D4 |
| 28 | `katas-multiagent-error-propagation` | Propagación de errores multi-agente: access failure vs valid empty, local recovery, coverage gap. | `multiagent error propagation, access failure vs empty, coverage gap, local recovery` | D1 |
| 29 | `katas-confidence-stratified-sampling` | Confidence calibration contra labeled set + stratified sampling; accuracy desglosada, no agregada. | `confidence calibration, stratified sampling, calibrated confidence, accuracy by segment` | D4 |
| 30 | `katas-false-positive-criteria` | Criterios categóricos con ejemplos +/- para reducir falsos positivos; disable temporal por categoría. | `false positive criteria, categorical criteria, fp rate by category, explicit criteria` | D4 |

## Contrato CI por skill (recordatorio Fase E/F)

Cada skill `katas-*` debe pasar `validate-skills.py --strict`:
1. **16 archivos canónicos** (SKILL.md, README.md, agents/{lead,support,guardian,specialist}.md, knowledge/{body-of-knowledge.md,knowledge-graph.json}, prompts/{primary,meta}.md, prompts/variations/{quick,deep}.md, templates/output.md, evals/evals.json, examples/{example-input,example-output}.md).
2. **Frontmatter** `name`, `version`, `description` (name == slug).
3. **allowed-tools** dentro de whitelist {Bash, Edit, Glob, Grep, MultiEdit, NotebookEdit, Read, Task, TodoWrite, WebFetch, WebSearch, Write}.
4. **JSON válido** en evals.json y knowledge-graph.json.
5. **Sin links markdown relativos rotos** dentro de los `.md` de la skill (usar backticks para nombres de skills relacionadas, NO `[x](../x)`).

> El scaffolder `scripts/scaffold-skill.py` genera estructura CI-válida por defecto; los agentes de Fase E SOLO enriquecen contenido con la kata, preservando frontmatter y sin introducir links rotos.

## Mapeo a mejoras de infraestructura (Fase D)

| Mejora Fase D | Skills relacionadas |
|---------------|---------------------|
| `pre-tool-guard.sh` policy-driven + `references/guardrails/*.json` | 02 |
| `references/reliability/prefix-caching.md` | 10, 14, 18 |
| `references/reliability/context-dilution.md` | 11, 12 |
| `references/schemas/annotations.schema.json` + `scripts/post_annotations.py` + `validate.yml` | 05, 13 |
| `scripts/batch/batch-runner.py` | 17 |
| manifiesto path-rules | 09 |
| check WARN descripción en `validate-skills.py` | 21 |
| `scripts/qa/run-adversarial-tests.py` (stratified + FP) | 29, 30 |
