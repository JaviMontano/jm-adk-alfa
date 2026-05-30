#!/bin/bash
# One-off: scaffold the 30 katas-* skills (Fase E pre-step). Idempotent-ish:
# scaffold-skill.py refuses to overwrite an existing skill dir without --force.
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

# slug|description|triggers
ROWS=$(cat <<'EOF'
katas-deterministic-agent-loop|Control de bucle agentico por stop_reason tipado (tool_use vs end_turn), nunca por prosa del modelo; halt y budget deterministas.|deterministic loop, stop_reason, agent loop control, budget exceeded
katas-pretooluse-guardrails|Guardarrailes deterministas en hook PreToolUse con permissionDecision deny desde politica recargable, no en el system prompt.|pretooluse guardrail, permission decision, policy gate, deterministic guardrail
katas-posttooluse-normalization|Normalizacion de outputs heterogeneos via hook PostToolUse y updatedMCPToolOutput antes de entrar al historial del modelo.|posttooluse normalization, output normalization, updatedmcptooloutput, legacy payload
katas-hub-and-spoke-isolation|Aislamiento multi-agente con AgentDefinition y built-in Task; cada subagente arranca con contexto vacio y modelo propio.|hub and spoke, subagent isolation, agentdefinition, task tool isolation
katas-defensive-structured-extraction|Extraccion defensiva con JSON Schema, tool_choice forzado, enums con valvula de escape y nullable explicito; nunca prosa.|defensive extraction, json schema extraction, forced tool_choice, nullable union
katas-mcp-structured-errors|Errores MCP tipados (isError, errorCategory, isRetryable, retryAfterSeconds); la politica de retry vive en el cliente.|mcp structured error, error category, retryable error, typed error contract
katas-plan-mode-exploration|Exploracion segura en Plan Mode read-only con plan.md firmado por humano antes de transicionar a escritura.|plan mode, read-only exploration, plan approval, safe exploration
katas-hierarchical-claude-memory|Memoria jerarquica CLAUDE.md user/team/module con at-imports y precedencia por especificidad de subpath.|hierarchical memory, claude md memory, memory imports, memory precedence
katas-path-conditional-rules|Reglas condicionales por glob de ruta; universales siempre cargadas, heuristicas de lenguaje on-demand.|path conditional rules, glob rules, conditional memory, per-path rules
katas-prefix-caching|Prefix caching: estatico-first y dinamico-last; interpretar cache_creation vs cache_read input tokens para estimar ahorro.|prefix caching, kv cache, cache control, static prefix
katas-context-dilution-mitigation|Mitigacion de dilucion softmax: edge placement de reglas criticas y compactacion al cruzar 50-60 por ciento de contexto.|context dilution, lost in the middle, edge placement, context compaction
katas-multipass-prompt-chaining|Prompt chaining multi-pass: pase local tipado por unidad y pase de integracion que solo ve resumenes, no las unidades crudas.|prompt chaining, multipass chaining, local then integrate, chaining schema
katas-headless-code-review|Code review headless con claude -p output-format json validado contra schema; el humano sigue siendo gate final de merge.|headless code review, claude p json, output format json, ci annotations
katas-fewshot-edge-calibration|Few-shot para calibrar bordes subjetivos con 2-4 ejemplos del mismo schema; complementa, no reemplaza, al schema.|few-shot calibration, edge examples, fewshot prompting, subjective calibration
katas-critical-self-correction|Evaluacion critica: cross-check numerico declarado vs calculado, mismatch flag con ambos valores, sin corregir en silencio.|critical self-correction, numeric cross-check, mismatch flag, computed vs stated
katas-human-handoff-protocol|Handoff a humano con payload tipado autocontenido (customer_id, issue_summary, actions_taken); end-state del bucle, no pausa.|human handoff, escalate to human, handoff payload, escalation protocol
katas-message-batch-processing|Procesamiento masivo con Message Batches API, custom_id unico por request y fragmentacion selectiva de fallos parciales.|message batches, batch processing, custom_id, offline batch
katas-persistent-scratchpad|Scratchpad persistente en disco curado por el agente; sobrevive a compact y reinicios, leido una vez y referenciado despues.|persistent scratchpad, investigation scratchpad, durable memory, scratchpad file
katas-adaptive-investigation|Investigacion adaptativa: mapeo barato, budget de exploracion acotado y re-plan disciplinado solo al invalidar la hipotesis.|adaptive investigation, dynamic decomposition, exploration budget, re-plan discipline
katas-provenance-preservation|Provenance tipada: no hay claim sin source; conflictos marcados con conflict true y escalados, nunca promediados.|provenance preservation, claim source mapping, conflict flag, source provenance
katas-tool-description-quality|Calidad de descripciones de tools como contrato de seleccion; rename y split sobre overloading para evitar misroute.|tool description quality, tool routing ambiguity, rename split tools, tool contract
katas-mcp-server-configuration|Configuracion de MCP servers: project vs user scope, env-var expansion para credenciales y rotacion ante secreto leakeado.|mcp server configuration, mcp scope, env var credentials, mcp json config
katas-builtin-tool-selection|Seleccion de built-in tools con estrategia Grep then Read then Edit, failure modes y sin Read masivo upfront.|builtin tool selection, grep read edit, tool strategy, edit anchor
katas-custom-commands-skills|Slash commands vs skills: context fork, allowed-tools whitelist y argument-hint; convenciones permanentes van en CLAUDE.md.|custom slash commands, skills frontmatter, context fork skill, command vs skill
katas-session-resume-fork|Gestion de sesiones: resume vs fork vs fresh con summary tipado; detectar cuando los tool results estan stale.|session resume, session fork, fresh summary session, stale tool results
katas-validation-retry-feedback|Validacion y retry con error feedback especifico; distinguir recuperable de no recuperable; max 2-3 intentos y luego escalar.|validation retry, error feedback loop, retry with feedback, recoverable error
katas-independent-reviewer-multipass|Multi-pass review con reviewer independiente en sesion limpia; per-file y cross-file; rechazo de quorum N-de-M.|independent reviewer, multipass review, self-review bias, per-file cross-file
katas-multiagent-error-propagation|Propagacion de errores multi-agente: distinguir access failure de valid empty, local recovery primero y coverage gap annotation.|multiagent error propagation, access failure vs empty, coverage gap, local recovery
katas-confidence-stratified-sampling|Confidence calibration contra labeled set y stratified sampling por document_type; accuracy desglosada, nunca agregada.|confidence calibration, stratified sampling, calibrated confidence, accuracy by segment
katas-false-positive-criteria|Criterios categoricos con ejemplos positivos y negativos por severidad para reducir falsos positivos; disable temporal por categoria.|false positive criteria, categorical criteria, fp rate by category, explicit criteria
EOF
)

count=0
while IFS='|' read -r slug desc triggers; do
  [ -z "$slug" ] && continue
  if [ -d "skills/$slug" ]; then
    echo "skip (exists): $slug"
    continue
  fi
  python3 scripts/scaffold-skill.py \
    --name "$slug" \
    --description "$desc" \
    --triggers "$triggers" \
    --allowed-tools "Read,Grep,Glob,Bash" \
    --owner "JM Labs" \
    --version "1.0.0" \
    --apply >/dev/null
  count=$((count + 1))
  echo "scaffolded: $slug"
done <<< "$ROWS"

echo "done: scaffolded $count katas-* skills"
