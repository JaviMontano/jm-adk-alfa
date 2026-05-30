#!/bin/bash
# One-off: scaffold the 22 competency skills (Etapa G). Idempotent: skips existing dirs.
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

# slug|description|triggers
ROWS=$(cat <<'EOF'
hook-engineering|Disenar hooks deterministas (PreToolUse permissionDecision deny, PostToolUse updatedMCPToolOutput) que el runtime garantiza, con politica recargable en codigo.|hook engineering, pretooluse hook, posttooluse hook, deterministic hooks
agentic-loop-engineering|Construir el bucle de control agentico que enruta por stop_reason tipado con budget duro y handlers explicitos, no por prosa.|agentic loop engineering, agent control loop, stop_reason routing, loop budget
subagent-orchestration|Orquestar coordinadores hub-and-spoke con AgentDefinition y Task, contexto aislado por subagente y propagacion de errores estructurada.|subagent orchestration, hub and spoke, coordinator agents, error propagation
structured-output-design|Disenar extraccion estructurada con JSON Schema defensivo: required reales, nullable union, enums con valvula de escape y tool_choice forzado.|structured output design, json schema output, defensive schema, forced tool_choice
mcp-engineering|Configurar MCP servers (project vs user scope, env-var expansion) y disenar contratos de error tipados con categoria y retryable.|mcp engineering, mcp server config, mcp error contract, mcp scope
tool-use-design|Disenar descripciones de tools como contrato de routing y aplicar la estrategia de built-in tools grep then read then edit.|tool use design, tool description contract, builtin tool strategy, tool routing
plan-mode-workflow|Operar repos desconocidos en Plan Mode read-only con plan firmado antes de escribir, aplicado por hooks.|plan mode workflow, read-only exploration, plan approval gate, two-mode operation
claude-md-architecture|Estructurar memoria jerarquica CLAUDE.md user/team/module con at-imports y reglas condicionales por glob de ruta.|claude md architecture, hierarchical memory, path scoped rules, memory imports
context-window-engineering|Ingenieria de ventana de contexto: prefix caching estatico-first y mitigacion de dilucion softmax con edge placement y compactacion.|context window engineering, prefix cache optimization, context dilution, edge placement
prompt-chaining-design|Descomponer tareas grandes en pase local tipado y pase de integracion sobre resumenes, con schemas de transicion entre pases.|prompt chaining design, multipass decomposition, transition schema, chained passes
few-shot-engineering|Disenar few-shot que calibra bordes subjetivos con 2-4 ejemplos del mismo schema, al inicio para preservar prefix cache.|few-shot engineering, edge calibration examples, fewshot design, subjective calibration
self-correction-loops|Construir verificacion cruzada declarado vs calculado con mismatch flag y escalada; nunca corregir numeros en silencio.|self-correction loops, cross-check verification, mismatch flag, numeric validation
human-escalation-design|Disenar handoff tipado a humano como end-state del bucle con payload autocontenido; no prosa de escalada.|human escalation design, typed handoff, escalation payload, escalate to human
message-batch-orchestration|Orquestar Message Batches API para cargas offline con custom_id unico y fragmentacion selectiva de fallos parciales.|message batch orchestration, offline batch, custom_id correlation, partial failure retry
persistent-memory-design|Disenar scratchpad persistente en disco con conclusiones validadas que sobrevive a compact, leido una vez y referenciado.|persistent memory design, scratchpad file, durable agent memory, investigation notes
adaptive-investigation-method|Investigar dominios desconocidos con mapeo barato, budget acotado y re-plan disciplinado solo al invalidar la hipotesis.|adaptive investigation method, dynamic decomposition, exploration budget, disciplined replan
provenance-engineering|Preservar provenance tipada con invariante no hay claim sin source y conflictos marcados y escalados, no promediados.|provenance engineering, claim source invariant, conflict marking, typed provenance
custom-tooling-extension|Extender Claude Code con slash commands y skills usando context fork, allowed-tools whitelist y argument-hint, con scope correcto.|custom tooling extension, slash command authoring, skill frontmatter, context fork
session-lifecycle-management|Decidir resume vs fork vs fresh con summary tipado segun validez de contexto y deteccion de tool results stale.|session lifecycle management, resume vs fork, fresh summary session, stale context
validation-retry-design|Disenar loop de validacion y retry con error feedback especifico, distinguiendo recuperable de no recuperable, con tope y escalada.|validation retry design, error feedback loop, recoverable vs not, retry budget
independent-review-design|Disenar revision con reviewer independiente en sesion limpia, pases per-file y cross-file, sin quorum que suprima senal rara.|independent review design, clean session reviewer, per-file cross-file, no quorum
evaluation-confidence-design|Disenar evaluacion con confidence calibrada contra labeled set, stratified sampling y criterios categoricos para reducir falsos positivos.|evaluation confidence design, confidence calibration, stratified sampling, false positive criteria
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

echo "done: scaffolded $count competency skills"
