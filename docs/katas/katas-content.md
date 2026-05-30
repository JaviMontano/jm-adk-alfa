# Katas Content — Claude Certified Architect (fuente canónica)

> Extraído de `katas.pdf` (Raúl A. Alzate · "Katas Practice Pocket Guide" · 30 katas, 5 dominios, 6 escenarios).
> Esta es la **fuente de verdad legible por máquina** para generar las 30 skills `katas-*`.
> Convención: prosa en español, identificadores de código en inglés. Evidencia: todo proviene del PDF `[DOC]`.

## Dominios y peso de examen

| Dominio | Tema | Peso | Katas |
|---|---|---:|---|
| D1 · Agentic Architecture | Bucles, hooks, subagentes | 27% | 01, 02, 03, 04, 13, 16, 19, 28 |
| D2 · Tool Design & MCP | Tools, errores, MCP | 18% | 05, 06, 21, 22, 23 |
| D3 · Claude Code Config | CLAUDE.md, skills, plan mode | 20% | 07, 08, 09, 24, 25 |
| D4 · Prompt & Structured Output | Schemas, few-shot, batch | 20% | 14, 15, 17, 26, 27, 29, 30 |
| D5 · Context & Reliability | Contexto, escalación, provenance | 15% | 10, 11, 12, 18, 20 |

## 6 escenarios oficiales

Customer Support · Code Generation · Multi-Agent · Dev Productivity · CI/CD · Structured Extract. (el examen presenta 4 de 6 al azar; las preguntas son scenario-aware.)

## Leyenda

- **⚠ por qué importa** — la falla real que evita.
- **✓ argumento** — lo que el arquitecto defiende.
- **✗ anti-patrón** — el error trampa.
- **quiz** — clave de respuestas oficial (Apéndice B).

---

## D1 · Agentic Architecture

### Kata 01 · Bucle agéntico determinista
- **slug:** `katas-deterministic-agent-loop` · **escenarios:** Customer Support, Multi-Agent Research
- **Qué es:** Bucle que decide continuar/detenerse mirando SOLO el campo estructurado `stop_reason` (tool_use vs end_turn), nunca la prosa del modelo.
- **⚠ Evita:** Detener por heurística de texto convierte una frase casual ("task complete") en halt silencioso o, peor, bucle infinito cuando el modelo nunca dice la frase.
- **Modelo mental:** cada iteración produce un `stop_reason` (`tool_use`→dispatch, `end_turn`→halt, otros→error explícito). `tool_result` vuelve como `role=user`, manteniendo contrato turn-by-turn. `max_tokens`/`pause_turn` inesperados deben fallar fuerte, no silencioso.
- **GOOD:** `while True: resp=create(...); if resp.stop_reason=="tool_use": dispatch+continue; elif "end_turn": return; else: raise UnhandledStop(resp.stop_reason)`.
- **✗ ANTI:** `DONE=["task complete","done","listo"]; if any(p in text for p in DONE): return` — parsea prosa.
- **✓ argumento:** el control del bucle vive en `stop_reason` + budget + handlers tipados, no en heurísticas de texto.
- **quiz:** B·B·B (P3: limitar iteraciones con budget configurable, e.g. `max_iterations`, y elevar `BudgetExceeded`).

### Kata 02 · Guardarrailes deterministas con PreToolUse
- **slug:** `katas-pretooluse-guardrails` · **escenarios:** Customer Support, Financial Compliance
- **Qué es:** Hook PreToolUse registrado en `ClaudeAgentOptions.hooks` inspecciona `tool_name`+`tool_input` ANTES de ejecutar y emite `permissionDecision:'deny'` cuando una política externa (dict/JSON) lo dicta.
- **⚠ Evita:** Pedir en system prompt "no aprueben reembolsos > $1000" es sugerencia; un prompt injection o usuario insistente la rompe y la tool ejecuta igual.
- **Modelo mental:** la política vive en código (dict recargable), no en el prompt. El SDK garantiza que la tool NO corre si el hook retorna deny; el modelo recibe el motivo y replanea. `permissionDecision` es estructurado (allow/deny/ask). Complementa al `stop_reason` del Kata 01.
- **GOOD:** `POLICY={"max_amount":1000.0}; async def policy_gate(input,tool_use_id,ctx): if amount>POLICY["max_amount"]: return {"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":...}}`. Hook registrado: `hooks={"PreToolUse":[HookMatcher(matcher="*",hooks=[policy_gate])]}`.
- **✗ ANTI:** política solo en `system_prompt` + sin hooks → prompt injection la rompe.
- **✓ argumento:** las políticas críticas (límites monetarios, dominios prohibidos, paths protegidos) viven en hooks PreToolUse con `permissionDecision` estructurado, no en system prompts.
- **quiz:** B·C·B (P2: modificar dict POLICY o recargar JSON, hot-reload, sin reiniciar el agente; P3: `deny` corre ANTES de ejecutar la tool = cero side-effects, `raise` corre DESPUÉS).

### Kata 03 · Normalización con PostToolUse
- **slug:** `katas-posttooluse-normalization` · **escenarios:** Customer Support, Legacy ERP Integration
- **Qué es:** Hook PostToolUse intercepta `tool_response` heterogéneo (XML legacy, códigos arcanos) y lo reescribe a JSON canónico vía `updatedMCPToolOutput` antes de que entre al historial del modelo.
- **⚠ Evita:** Sin normalización central, cada token de XML legacy quema budget y dispersa atención; normalizar por-tool es frágil (cualquier wrapper nuevo que olvide la regla rompe la garantía).
- **Modelo mental:** PostToolUse es runtime garantizado, no convención del autor de la tool. `updatedMCPToolOutput` reemplaza el output crudo; el modelo nunca ve el XML. `STATUS_MAP`/esquemas de traducción viven en código recargable. `additionalContext` anexa metadatos auditables sin contaminar el payload limpio.
- **GOOD:** `STATUS_MAP={"0xA1":"paid",...}; async def normalize_legacy(input,tool_use_id,ctx): clean={...}; return {"hookSpecificOutput":{"hookEventName":"PostToolUse","updatedMCPToolOutput":{...json.dumps(clean)...}}}`.
- **✗ ANTI:** cada tool decide si normaliza con `@tool` decorators; un handler nuevo olvida y envenena el contexto.
- **✓ argumento:** la normalización de outputs heterogéneos es responsabilidad del runtime vía PostToolUse, no convención de cada tool.
- **quiz:** C·B·B (P1: el runtime SDK garantiza normalización para TODAS las tools que matcheen; P2: `additionalContext` para metadatos auditables que el modelo no necesita ver).

### Kata 04 · Aislamiento hub-and-spoke con subagentes
- **slug:** `katas-hub-and-spoke-isolation` · **escenarios:** Multi-Agent Research, Code Audit Pipeline
- **Qué es:** Registrar subagentes como `AgentDefinition` en `ClaudeAgentOptions.agents` y despacharlos vía built-in Task tool. Cada invocación abre una sesión nueva con su propio `system_prompt`, tools y modelo; el coordinador recibe SOLO el último mensaje como `tool_result`.
- **⚠ Evita:** Pasar todo el historial del coordinador a cada subagente diluye atención, filtra políticas que no debería ver, multiplica costo y aumenta blast radius de prompt injection.
- **Modelo mental:** hub-and-spoke: coordinador despacha, especialistas ejecutan con contexto vacío. Cada Task = sesión nueva (aislamiento estructural por runtime). Cada subagente puede tener tools, system_prompt y modelo distintos (haiku barato para extracción). El coordinador agrega solo el último mensaje, no el historial interno.
- **GOOD:** `extractor=AgentDefinition(description="Extrae hechos de UN documento",prompt="...",tools=[],model="haiku"); options=ClaudeAgentOptions(agents={"extractor":extractor},allowed_tools=["Task"],max_turns=15)`.
- **✗ ANTI:** un solo agente con TODO concatenado, sin agents, sin Task → contexto diluido, políticas cruzadas, modelo único caro.
- **✓ argumento:** el aislamiento entre tareas multi-agente es estructural vía AgentDefinition+Task, no convencional vía system prompt; cada Task es sesión nueva por construcción del SDK.
- **quiz:** B·B·B (blast radius acotado por aislamiento; modelo distinto por subagente vía AgentDefinition).

### Kata 13 · Code Review Headless en CI/CD
- **slug:** `katas-headless-code-review` · **escenarios:** CI/CD Automation
- **Qué es:** Claude Code corre en CI sin TTY (`claude -p`) y produce JSON estructurado con anotaciones por línea (`file,line,severity,rule_id,message`). El pipeline valida con schema declarado y publica comentarios deterministas en el PR. Cero parsing de prosa libre.
- **⚠ Evita:** Un reviewer humano no escala a 100 PRs/día. Un reviewer LLM en CI encuentra issues consistentes, pero solo si su salida es estructurada. Si se parsea prosa con regex, el pipeline rompe el primer día que el modelo cambie de redacción o idioma.
- **Modelo mental:** `claude -p 'prompt' --output-format=json` produce JSON validable contra schema declarado. Schema: lista de Annotation `{file,line,severity,rule_id,message}`. Si no valida, el job falla, no se "ajusta". El humano sigue siendo gate final de merge: el LLM anota, no aprueba.
- **GOOD:** `.github/workflows/review.yml`: `claude -p "$REVIEW_PROMPT" --output-format=json --schema annotations.schema.json > out.json; python scripts/post_annotations.py out.json`.
- **✗ ANTI:** `claude -p "$REVIEW_PROMPT" > review.txt; grep -E 'ERROR|WARNING|issue' | awk ... | xargs gh pr comment` — parsea prosa.
- **✓ argumento:** flag `--output-format=json` + validación con schema (extracción defensiva, Kata 5) + control por señal (Kata 1); el humano sigue siendo gate final de merge.
- **quiz:** B·C·B (P2: si el JSON no valida, el job falla, no se publican comentarios; humano investiga; P3: el LLM puede tener FP/FN y no asume responsabilidad legal del merge).

### Kata 16 · Protocolo de Handoff a Humano
- **slug:** `katas-human-handoff-protocol` · **escenarios:** Customer Support
- **Qué es:** Cuando el agente toca una política que no puede resolver (límite excedido, decisión irreversible, conflicto de datos), invoca la tool `escalate_to_human`, suspende la generación de prosa y emite un payload JSON estricto: `customer_id, issue_summary, actions_taken, escalation_reason, recommended_action`.
- **⚠ Evita:** Pasar al humano un transcript crudo es desastre operacional: el operador tiene que leer todo, adivinar contexto y decidir bajo presión. Un payload tipado autocontenido reduce tiempo de resolución y elimina ambigüedad.
- **Modelo mental:** detectar precondición (límite/irreversibilidad/conflicto) → llamar tool `escalate_to_human`; corta generación de texto. Payload autocontenido: el humano NO debe necesitar leer la conversación previa. Es un end-state del bucle, no una pausa: el agente no continúa hasta que el humano resuelve.
- **GOOD:** `if refund_amount>tier2_limit: return tool_call('escalate_to_human',{customer_id,issue_summary,actions_taken,escalation_reason,recommended_action})`.
- **✗ ANTI:** `return 'Lo siento, ese reembolso supera mi límite. Voy a hablar con mi supervisor...'` + sigue generando prosa.
- **✓ argumento:** enumerar precondiciones de escalada (límite, irreversibilidad, conflicto); la salida del handoff es tipada y autocontenida; conecta con Kata 2 (hook puede forzar ask_human) y Kata 15 (mismatch numérico dispara handoff).
- **quiz:** B·B·B (P3: hook PostToolUse que termine la sesión tras escalate_to_human; el handoff es end-state, no pausa).

### Kata 19 · Investigación Adaptativa (Descomposición Dinámica)
- **slug:** `katas-adaptive-investigation` · **escenarios:** Multi-Agent Orchestration, Dev Productivity, Code Generation
- **Qué es:** En dominio desconocido no se planifica al detalle de antemano: el agente mapea topología primero (glob de nombres, regex de imports/símbolos), genera un plan priorizado, y re-adapta cuando un hallazgo invalida el plan vigente. Todo dentro de un presupuesto de exploración acotado.
- **⚠ Evita:** Un plan rígido en territorio desconocido garantiza desperdicio: el agente sigue ramas muertas porque "estaba en el plan". Adaptar dinámicamente prioriza atención sobre lo que la realidad muestra, no lo que la hipótesis inicial asumía.
- **Modelo mental:** Fase 1 mapeo barato (glob de nombres). Fase 2 priorización declarada. Fase 3 deep-dive solo sobre priorizados. Re-planificar SOLO si un hallazgo INVALIDA el plan (no si solo lo refina); evita loops de re-planificación reflejos. Presupuesto duro: máximo de archivos/queries/minutos. Persistir plan y findings en scratchpad (Kata 18).
- **GOOD:** `topology=scan_repo(globs=['src/**/*.py']); budget=Budget(files=50,queries=20); plan=prioritize(topology); while plan and budget.remaining(): target=plan.pop(); finding=deep_dive(target,budget); scratchpad.append('Hallazgos',finding); if finding.invalidates(plan): plan=re_plan(topology,finding)`.
- **✗ ANTI:** `plan=make_full_plan_upfront(repo); for task in plan: do(task)` — no actualiza nunca; o `read_all_files()` sin budget; o re_plan() en cada turno por reflejo.
- **✓ argumento:** definir presupuesto de exploración; enunciar el criterio de re-planificación (que dispara un re-plan, qué no); conectar con Kata 4 (subagentes para deep-dive paralelo) y Kata 18 (scratchpad).
- **quiz:** C·B·B (P1: mapeo barato→priorización→deep-dive selectivo→re-plan invalida; P3: reportar lo encontrado y pendientes, escalar a humano con scratchpad como evidencia).

### Kata 28 · Propagación de Errores Multi-Agente
- **slug:** `katas-multiagent-error-propagation` · **escenarios:** Customer Support, Multi-Agent
- **Qué es:** En hub-and-spoke los errores se propagan al coordinador con contexto estructurado: `failure_type, attempted_query, partial_results, suggested_alternatives`. Cuatro reglas: local recovery primero; distinguir access failure de valid empty; coverage gap annotation; nunca enmascarar error como success vacío.
- **⚠ Evita:** Devolver `{results:[]}` en un timeout hace que el coordinador asuma "no había info" y produzca un report confiado con hueco silencioso. Genérico 'search unavailable' priva al coordinador del contexto para decidir alternativas.
- **Modelo mental:** local recovery primero (subagente reintenta transients antes de propagar). Access failure (timeout, permission) != valid empty (search OK, 0 matches). Coverage gap annotation explícita en el synthesis. Nunca enmascarar error como success vacío.
- **GOOD:** subagente: `try: results=http_search(query,timeout=10); if not results: return {"success":True,"results":[],"empty_valid":True}; return {"success":True,"results":...} except TimeoutError: try broaden(); except: return {"success":False,"failure_type":"timeout","attempted_query":...,"partial_results":[],"suggested_alternatives":[...]} except PermissionError as e: return {"success":False,"failure_type":"permission","retryable":False,"explanation":str(e)}`.
- **✗ ANTI:** `except Exception: return {"results":[]}` — enmascara error como success vacío.
- **✓ argumento:** distinguir access failure de valid empty; defender local recovery + propagación estructurada; insistir en coverage gap annotation; rechazar enmascarar errores como success vacío.
- **quiz:** B·B·C (P2: local recovery primero, broaden/longer-timeout; P3: `retryable=false` (permission) = señal explícita, escalar/anotar coverage gap, no reintentar misma query).

---

## D2 · Tool Design & MCP

### Kata 05 · Extracción estructurada defensiva con JSON Schema
- **slug:** `katas-defensive-structured-extraction` · **escenarios:** Structured Extraction, Customer Support
- **Qué es:** Forzar `tool_choice` con un JSON Schema que declara `required` reales, opcionales como union nullable, y enums con válvula de escape (`'other'`,`'unclear'`) acompañada de un campo `details`.
- **⚠ Evita:** Pedir "devuélveme JSON" en prosa garantiza alucinación silenciosa: inventar campos faltantes, llenar vacíos con `''` o forzar valores fuera de dominio.
- **Modelo mental:** `required`=siempre presente en la fuente; si no, marca nullable union. Default `''` es alucinación: si no sabe, debe ser `null` o `'unclear'`. Enums sin escape obligan a mentir cuando el valor no encaja. `tool_choice` forzado evita 'best-effort prosa'.
- **GOOD:** `EXTRACT_TOOL={"name":"extract_invoice","input_schema":{"type":"object","required":["invoice_id","currency","status"],"properties":{"invoice_id":{"type":"string"},"currency":{"type":"string","enum":["USD","EUR","COP","other"]},"currency_other_details":{"type":["string","null"]},"status":{...},"due_date":{"type":["string","null"],"format":"date"}}}}; create(tools=[EXTRACT_TOOL],tool_choice={"type":"tool","name":"extract_invoice"})`.
- **✗ ANTI:** prompt en prosa "devuelve JSON con invoice_id..." + `json.loads(resp.text)`.
- **✓ argumento:** extracción usa tool_choice forzado + schema con required reales + enums con escape + nullable explícito; nunca prosa.
- **quiz:** B·B·B (P1: nullable union `{"type":["string","null"],"format":"date"}`; P2: enum con `'other'`+campo details; P3: NO forzar tool_choice cuando el modelo decide entre varias tools o cuando puede responder híbrido).

### Kata 06 · Errores estructurados en MCP
- **slug:** `katas-mcp-structured-errors` · **escenarios:** Customer Support, API Integration Reliability
- **Qué es:** Un servidor MCP que falla devuelve un payload tipado con `isError, errorCategory, isRetryable, retryAfterSeconds`; el agente decide retry, escalada o aborto leyendo los flags, no la prosa del error.
- **⚠ Evita:** Un string genérico 'something went wrong' obliga al modelo a adivinar: reintenta para siempre, abandona, o escala casos que solo necesitaban backoff.
- **Modelo mental:** tres ejes: ¿es error? ¿es reintentable? ¿qué categoría (auth, rate_limit, not_found, validation, transient)? El agente lee flags, no prosa. `explanation` es para el humano que audita el log, no para el modelo. Las políticas de retry (backoff exponencial, n máximo) viven en el cliente, no en el modelo.
- **GOOD:** `except RateLimitException as e: return {"isError":True,"errorCategory":"rate_limit","isRetryable":True,"retryAfterSeconds":e.retry_after,"explanation":...}`. Cliente: `if result.get("isError") and result.get("isRetryable"): time.sleep(result["retryAfterSeconds"]); return retry(args); if errorCategory=="auth": return escalate_to_human(result)`.
- **✗ ANTI:** `except Exception as e: return {"error":f"failed: {e}"}` — string genérico.
- **✓ argumento:** los errores de MCP son contratos tipados (isError, errorCategory, isRetryable); la política de retry vive en el cliente, no en el modelo.
- **quiz:** B·B·B (P2: `transient`=backoff exponencial, `rate_limit`=espera `retryAfterSeconds` exacto; P3: error sin categoría → tratar como non-retryable, categorizar 'unknown', loggear).

### Kata 21 · Calidad de Descripciones de Tools
- **slug:** `katas-tool-description-quality` · **escenarios:** Customer Support, Multi-Agent, Dev Productivity
- **Qué es:** La descripción de un tool es el único mecanismo que el modelo usa para escoger entre tools similares. Buenas descripciones incluyen input format, ejemplos de query y la frontera explícita ("usa esto en lugar de X cuando...").
- **⚠ Evita:** Cuando dos tools tienen descripciones genéricas ('Analyzes content','Analyzes documents'), el modelo enruta mal en 20–30% de turnos. El síntoma es 'respuesta razonable pero del tool incorrecto', invisible en logs hasta que un downstream rompe.
- **Modelo mental:** descripción = contrato de uso; contratos solapados = ambiguos por diseño. Renombrar suele superar a 'explicar más' cuando el nombre confunde (`analyze_content`→`extract_web_results`). Splitting beats overloading: cinco tools con un propósito > uno con cinco modos. El system prompt interactúa con la descripción: keywords pueden sesgar el routing.
- **GOOD:** `{"name":"extract_web_results","description":"Parses HTML pages from a search query into a list of {title,url,snippet}. Use when input is a URL or raw HTML; for PDF/DOCX use parse_document instead."}` + `parse_document` con frontera recíproca.
- **✗ ANTI:** `[{"name":"analyze_content","description":"Analyzes content"},{"name":"analyze_document","description":"Analyzes documents"}]`.
- **✓ argumento:** la descripción es el árbitro de selección; identificar tools ambiguos por contrato solapado; proponer rename + split antes que 'explicar más'; detectar keywords del system prompt que sesgan el routing.
- **quiz:** B·B·C (P1: rename + descripción con input format + frontera; P2: split en tres tools con propósito único; P3: enunciar explícitamente en la descripción 'para temas regulatorios internos usa search_internal_docs aunque mencionen compliance').

### Kata 22 · Configuración de MCP Servers
- **slug:** `katas-mcp-server-configuration` · **escenarios:** Customer Support, Dev Productivity
- **Qué es:** MCP servers se declaran en `.mcp.json` (project, versionado) o `~/.claude.json` (user, personal). Credenciales se inyectan vía env-var expansion (`${GITHUB_TOKEN}`), nunca hardcoded. Múltiples servers se descubren simultáneamente.
- **⚠ Evita:** Hardcodear token en `.mcp.json` versionado equivale a publicarlo. Poner reglas de equipo en `~/.claude.json` deja a nuevos devs sin acceso. La elección de scope decide si funciona en toda la flota o solo en tu laptop.
- **Modelo mental:** project scope (`.mcp.json`) viaja con el repo; descubrimiento automático al conectar. User scope (`~/.claude.json`) es para experimentos personales que no afectan al equipo. Credenciales siempre por `${ENV_VAR}`, no literal. MCP resources (catálogos) reducen llamadas exploratorias frente a tools.
- **GOOD:** `.mcp.json`: `{"mcpServers":{"github":{"command":"npx","args":["-y","@modelcontextprotocol/server-github"],"env":{"GITHUB_TOKEN":"${GITHUB_TOKEN}"}},"internal-docs":{"command":"node","args":["./scripts/mcp-docs.js"]}}}`.
- **✗ ANTI:** `env:{"GITHUB_TOKEN":"ghp_AbCdEfG123456789"}` literal en archivo versionado.
- **✓ argumento:** distinguir project vs user scope con criterio; defender env-var expansion para credenciales; justificar MCP solo cuando un built-in no aplica; responder a un secreto leakeado con rotación + purga de history (filter-repo), no gitignore.
- **quiz:** B·C·C (P1: project scope versionado con `${CRM_TOKEN}`; P2: Grep built-in cubre búsqueda en filesystem local, MCP es overkill; P3: rotar credencial + reemplazar por `${ENV}` + purgar git history, gitignore NO remueve versionados).

### Kata 23 · Selección de Built-in Tools
- **slug:** `katas-builtin-tool-selection` · **escenarios:** Dev Productivity, Code Gen
- **Qué es:** Claude Code expone Grep (regex sobre contenido), Glob (patrones de path), Read (cargar archivo), Edit (mod dirigida con anchor único), Write (sobrescribir) y Bash. Cada uno tiene un uso primario y un failure mode. Estrategia incremental: Grep → Read → Edit.
- **⚠ Evita:** Read sobre todo el repo carga miles de tokens innecesarios. Edit con anchor no único falla. Saber qué tool aplica es mecánica básica del examen y diferencia agentes eficientes de agentes que queman contexto.
- **Modelo mental:** Grep=buscar contenido. Glob=buscar paths. Read=cargar archivo. Edit=mod puntual. Write=reescribir. Bash=shell. Estrategia: Grep primero (entry points) → Read selectivo (seguir imports) → Edit/Write puntual. Edit failure mode: anchor no único o no existente → falla. Fallback: Read entero + Write completo. Nunca 'leer todo el repo upfront'.
- **GOOD:** `matches=grep(pattern="processRefund\\(",glob="**/*.py"); content=read(matches[0].path); edit(path=matches[0].path,old_text="if amount > 1000:",new_text="if amount > MAX_REFUND:")`.
- **✗ ANTI:** `all_files=glob("**/*"); for f: read(f) # 200k tokens` + `edit(old_text="if amount", ...) # multiples lineas matchean → falla`.
- **✓ argumento:** escoger tool correcto en decisión rápida; describir failure mode de Edit y fallback Read+Write; defender estrategia Grep → Read → Edit; rechazar Read masivo upfront.
- **quiz:** C·C·B (P1: Glob con `**/*.test.tsx` para listar paths por patrón de nombre; P2: ampliar anchor con contexto suficiente, Write como fallback explícito; P3: Grep authenticate/login/session → Read selectivo → seguir imports).

---

## D3 · Claude Code Config

### Kata 07 · Exploración segura con Plan Mode
- **slug:** `katas-plan-mode-exploration` · **escenarios:** Dev Productivity, Code Gen
- **Qué es:** Antes de modificar un repo desconocido, el agente entra en Plan Mode (solo-lectura). Explora, escribe un `plan.md` con hallazgos y arquitectura propuesta, y obtiene aprobación humana directa antes de transicionar a ejecución.
- **⚠ Evita:** Lanzar un agente con permisos de escritura sobre un repo desconocido es destrucción probabilística; el primer error borra archivos clave o reescribe convenciones, y recuperar es caro.
- **Modelo mental:** dos modos: read-only (Plan) y write (Direct). Transición explícita y registrada. En Plan Mode las herramientas de escritura están deshabilitadas, no desaconsejadas. El artefacto de aprobación es texto auditable (`plan.md` firmado), no un 'ok' verbal. Aprobación = firma + plan congelado; cambios al plan re-piden aprobación. Los hooks aplican el modo.
- **GOOD:** `options=ClaudeAgentOptions(permission_mode="plan",allowed_tools=["Read","Glob","Grep"],system_prompt="En Plan Mode: explora, mapea, redacta plan.md. NO escribas código."); # hook PreToolUse niega escritura: if tool_name in write_tools and mode=="plan": return permissionDecision deny`.
- **✗ ANTI:** `permission_mode="bypassPermissions",allowed_tools=["Read","Write","Edit","Bash"]` desde el inicio.
- **✓ argumento:** Plan Mode es un contrato de dos modos read-only/write con transición firmada por humano, no un 'modo de cortesía'; los hooks aplican el modo.
- **quiz:** B·B·B (P2: volver a Plan Mode, actualizar plan.md, re-pedir aprobación; P3: hook PreToolUse que enumera tools de escritura -Write,Edit,NotebookEdit,Bash con redirecciones- y deniega).

### Kata 08 · Memoria jerárquica con CLAUDE.md
- **slug:** `katas-hierarchical-claude-memory` · **escenarios:** Dev Productivity, Code Gen
- **Qué es:** CLAUDE.md es la memoria persistente del agente en tres niveles que cargan en cascada: `~/.claude/CLAUDE.md` (usuario), `<repo>/CLAUDE.md` (equipo), `<repo>/<subpath>/CLAUDE.md` (módulo). Se compone modularmente con `@imports`.
- **⚠ Evita:** Repetir convenciones en cada prompt cuesta tokens y diverge entre miembros del equipo; sin una fuente de verdad por nivel, el agente improvisa y el equipo paga el costo.
- **Modelo mental:** más específico gana: `repo/src/CLAUDE.md` sobrescribe `repo/CLAUDE.md`. Lo personal (preferencias del usuario) NO va en el repo; va en el home. `@imports` mantienen el archivo principal corto y caché-friendly (Kata 10). Un CLAUDE.md monolítico de 2000 líneas degrada caché y dispersa atención.
- **GOOD:** `<repo>/CLAUDE.md`: `## Style @docs/style-guide.md` + `## Testing @docs/testing-conventions.md` + `## Forbidden - never run pip install without venv`. `~/.claude/CLAUDE.md`: preferencias personales (terse commits, ruff over black).
- **✗ ANTI:** mezclar preferencias personales en el repo + monolítico 2000 líneas con todo inline.
- **✓ argumento:** separación estricta usuario/equipo/módulo en CLAUDE.md y uso de @imports para modularidad y caché-friendliness.
- **quiz:** B·B·B (P2: modularizar vía @imports a archivos chicos en docs/; P3: precedencia subpath > repo > user para el scope del proyecto).

### Kata 09 · Reglas condicionales por ruta
- **slug:** `katas-path-conditional-rules` · **escenarios:** Dev Productivity, Code Gen
- **Qué es:** Reglas heurísticas (estilo, lints, convenciones de lenguaje) se cargan solo cuando el agente edita archivos que matchean un glob; reglas universales (seguridad) siempre cargadas.
- **⚠ Evita:** Un CLAUDE.md que carga 2000 líneas para todos los archivos paga el costo en todas las sesiones, incluso cuando el agente solo edita un README; cargar reglas Python solo al tocar `*.py` libera contexto para el resto.
- **Modelo mental:** la regla declara su glob de activación: `src/**/*.py`, `*.tf`. El agente carga la regla al entrar al archivo, la descarta al salir. Reglas grandes (heurísticas de lenguaje) → condicionales. Reglas universales (políticas de seguridad) → siempre cargadas.
- **GOOD:** `<repo>/CLAUDE.md`: `@rules/security.md  # universal, siempre` + `## When editing src/**/*.py: @rules/python-style.md @rules/python-testing.md` + `## When editing src/**/*.tf: @rules/terraform.md`. python-style NO se carga al editar README; security SÍ siempre.
- **✗ ANTI:** CLAUDE.md monolítico con todas las reglas (Python+Terraform+Go+Testing+Security) cargando siempre aunque solo edites README.
- **✓ argumento:** clasificación explícita de reglas como universales (siempre) o condicionales por glob, y estimación del ahorro de tokens medible.
- **quiz:** B·B·B (P1: universal = carga directa en CLAUDE.md raíz, sin glob; P2: ambas se cargan, más específica gana en conflictos puntuales -precedencia por subpath; P3: medir `input_tokens` editando README vs editando .py).

### Kata 24 · Slash Commands Custom y Skills
- **slug:** `katas-custom-commands-skills` · **escenarios:** Code Gen, Dev Productivity
- **Qué es:** Claude Code extiende la sesión con slash commands (`.claude/commands/X.md`, trigger `/X`) y skills (`.claude/skills/X/SKILL.md`, on-demand con frontmatter). Frontmatter de skill: `context: fork` (aísla en sub-agente), `allowed-tools` (whitelist), `argument-hint`.
- **⚠ Evita:** Commands en `~/.claude/commands/` no se replican al equipo. Skills sin `context: fork` contaminan la sesión principal con output verbose. Sin `allowed-tools`, una skill exploratoria puede escribir o borrar por accidente.
- **Modelo mental:** slash command = trigger explícito; skill = workflow on-demand con metadata. Project scope (`.claude/`) viaja con git; user scope (`~/.claude/`) es personal. `context: fork` aísla skill en sub-agente → economía de contexto. `allowed-tools` whitelist limita destructive ops por diseño. Convenciones siempre-aplicables van en CLAUDE.md, no en skill.
- **GOOD:** `.claude/skills/codebase-analysis/SKILL.md`: frontmatter `name, description, context: fork, allowed-tools: ["Read","Grep","Glob"], argument-hint: "<dir-or-feature>"` + body que Glob→Grep→devuelve resumen tipado.
- **✗ ANTI:** `~/.claude/skills/...` (user scope, no replica) + sin context fork (5000 tokens contaminan sesión principal) + sin allowed-tools (puede Write/Bash).
- **✓ argumento:** escoger command vs skill según trigger y scope; explicar frontmatter (context, allowed-tools, argument-hint); conectar context:fork con economía de contexto; defender CLAUDE.md para convenciones permanentes.
- **quiz:** B·B·C (P1: `.claude/commands/test-coverage.md` versionado; P2: `context:fork`+`allowed-tools:[Read,Grep,Glob]`; P3: convenciones siempre-aplicables van en CLAUDE.md, no en skill ni command).

### Kata 25 · Gestión de Sesiones (Resume y Fork)
- **slug:** `katas-session-resume-fork` · **escenarios:** Customer Support, Code Gen, Dev Productivity
- **Qué es:** Tres patrones de preservación de contexto: `--resume` continúa una sesión nombrada; `fork` crea ramas paralelas desde una baseline; sesión nueva con summary inyectado es preferible cuando tool results previos pueden estar stale.
- **⚠ Evita:** Resumir una sesión vieja con tool results stale lleva al modelo a referenciar archivos que ya no son lo que cree. Forks sin disciplina se mezclan asumiendo contexto compatible. Inyectar transcripts completos viejos infla contexto.
- **Modelo mental:** Resume = contexto válido, conversación sigue lógicamente. Fork = dos caminos desde misma baseline; cero interferencia entre ramas. Summary fresh = el mundo cambió; arrancar limpio con summary tipado en system prompt. Scratchpad estructurado (Kata 18) es la fuente natural del summary.
- **GOOD:** `claude --resume codebase-audit-2025-04` (misma investigación) · `claude --fork ... --new-name approach-A` (dos enfoques) · `SUMMARY=$(cat investigation-scratchpad.md); claude -p "Continuamos. Hallazgos previos:\n$SUMMARY"` (mundo cambió).
- **✗ ANTI:** resume después de refactor masivo (modelo recuerda archivos como eran, alucina); inyectar transcript completo viejo (infla contexto, reintroduce ruido).
- **✓ argumento:** decidir resume vs fork vs fresh con criterio; identificar cuándo los tool results están stale; conectar con scratchpad estructurado como fuente del summary; rechazar pegar transcripts completos viejos.
- **quiz:** B·C·B (P1: fresh con summary tipado del scratchpad inyectado en system prompt; P2: fork desde baseline a dos sesiones nombradas, cero interferencia; P3: fresh con summary del ticket + reload de fuentes actualizadas).

---

## D4 · Prompt & Structured Output

### Kata 14 · Few-Shot para Calibrar Bordes
- **slug:** `katas-fewshot-edge-calibration` · **escenarios:** Structured Extraction
- **Qué es:** Cuando la tarea es subjetiva (tono, formato no estándar, juicio estético), una descripción zero-shot deja al modelo en su default genérico. 2–4 ejemplos input/output desplazan su distribución hacia el formato deseado más rápido y barato que un párrafo de instrucciones.
- **⚠ Evita:** Decir 'responde en estilo casual chileno' no produce el resultado; mostrar 3 ejemplos de cómo se ve, sí. Few-shot es la forma más eficiente de comunicar ground truth para casos sin definición rígida, y se compone con schema (Kata 5).
- **Modelo mental:** los ejemplos son del mismo schema que la salida esperada; cubren los bordes del dominio, no el caso fácil. 2–4 suelen ser suficientes; >5 dispersa atención (Kata 11) y rompe caches (Kata 10) sin mejorar calidad. Few-shot complementa, no reemplaza, al schema: el schema impone forma, los ejemplos calibran juicio.
- **GOOD:** `prompt="Clasifica el ticket. Ejemplos:\nticket:'no me llega la factura desde hace 3 meses' clase:'billing',urgencia:'high'\nticket:'tengo una sugerencia para la app' clase:'feedback',urgencia:'low'\nticket:'no puedo entrar, token expirado' clase:'auth',urgencia:'high'\nahora clasifica:\nticket:'{user_text}'"`.
- **✗ ANTI:** párrafo abstracto "Clasifica usando criterio profesional, considerando urgencia, dominio, impacto, severidad operacional, prioridad SLA y política interna."
- **✓ argumento:** identificar cuándo few-shot supera a instrucciones en prosa; diseñar ejemplos que cubran bordes y no centro; combinar few-shot con schema (Kata 5) para tareas subjetivas con formato estricto sin saturar atención.
- **quiz:** B·B·B (P2: si few-shot contradice el schema, gana el schema -restricción sintáctica dura, re-escribir los ejemplos; P3: ejemplos al inicio = parte estática, maximiza prefix cache -Kata 10 y queda en borde de atención alta -Kata 11).

### Kata 15 · Evaluación Crítica y Auto-Corrección
- **slug:** `katas-critical-self-correction` · **escenarios:** Customer Support, Structured Extraction
- **Qué es:** Cuando el modelo extrae números (totales, sumas, fechas calculadas), debe cruzar lo calculado versus lo que la fuente declara. Si discrepan más allá de un epsilon, no decide arbitrariamente: emite un flag de conflicto con ambos valores y enruta a revisión humana.
- **⚠ Evita:** Un total de factura calculado por el modelo puede coincidir con el declarado, o no. Sin verificación cruzada, el sistema confía silenciosamente en la alucinación más plausible. En facturación/contabilidad/impuestos, eso es incidente operacional.
- **Modelo mental:** dos fuentes de verdad: lo declarado en el documento y lo calculado por el agente. Deben coincidir dentro de un epsilon. Si difieren, marcar `mismatch=true` con ambos valores y delta. Nunca 'elegir el más razonable'. Aplica a totales numéricos, sumas, conteos, fechas derivadas; mismatch escala vía Kata 16 (handoff humano).
- **GOOD:** `stated=extract_stated_total(doc); computed=sum(line.amount for line in doc.lines); if abs(stated-computed)>epsilon: return {"stated_total":stated,"computed_total":computed,"mismatch":True,"delta":stated-computed,"needs_human_review":True}`.
- **✗ ANTI:** `total=extract_total(doc) # confía en lo declarado` o `if abs(stated-computed)>epsilon: total=computed # corrige silenciosamente`.
- **✓ argumento:** identificar campos numéricos sujetos a verificación cruzada; definir epsilon de tolerancia (cero para enteros, epsilon pequeño para monedas) y justificarlo; conectar con Kata 16 (escalada humana) y Kata 20 (provenance).
- **quiz:** C·B·B (P1: marcar mismatch=true con ambos valores y escalar; P2: epsilon pequeño por redondeo de centavos -enteros cero, moneda redondeo; P3: si el doc no declara total, `computed_total` marcando `stated_total=null` y `mismatch=false`).

### Kata 17 · Procesamiento Masivo con Message Batches API
- **slug:** `katas-message-batch-processing` · **escenarios:** CI/CD Automation, Structured Extraction
- **Qué es:** Para cargas no interactivas (auditorías, backfills, evaluaciones), la Message Batches API procesa miles de requests offline a ~50% del costo. Cada request lleva un `custom_id` único que correlaciona request↔response y aísla fallos parciales.
- **⚠ Evita:** Pagar tarifa real-time por trabajo offline es desperdicio. Y procesar 10000 prompts uno por uno con un for rompe rate limits, no maneja fallos parciales y tarda horas. Batch es el patrón correcto: 50% ahorro, fail-isolation por request, escalable.
- **Modelo mental:** batch = colección de requests independientes con `custom_id` único por request. Ciclo: `create → poll processing_status → results`; el batch puede acabar 'ended' con éxitos parciales. Para fallos masivos, fragmentar en sub-batches y reintentar solo los failed (no todo el batch).
- **GOOD:** `batch=client.messages.batches.create(requests=[{"custom_id":f"audit-{i}","params":{...}} for i,_ in enumerate(items)]); while batch.processing_status!="ended": sleep(30); batch=retrieve(batch.id); for r in results(batch.id): save(r.custom_id,r.result)`.
- **✗ ANTI:** `for item in ten_thousand_items: r=client.messages.create(**params(item)); save(r)` — tarifa real-time, sin custom_id, rompe rate limits.
- **✓ argumento:** identificar cargas elegibles para Batch (offline, latency-tolerant); describir el ciclo create→poll→results; justificar la importancia del custom_id y la fragmentación selectiva para recuperación de fallos parciales.
- **quiz:** B·B·B (P1: Message Batches API con custom_id por ticket y polling; P2: sub-batch solo con los failed, identificados por custom_id; P3: custom_id es la única clave para mapear response↔input, duplicado=ambigüedad).

### Kata 26 · Validación y Retry con Error Feedback
- **slug:** `katas-validation-retry-feedback` · **escenarios:** CI/CD, Structured Extraction
- **Qué es:** Cuando una extracción tipada falla validación (Pydantic/JSON Schema), se hace retry-with-error-feedback: nueva llamada incluyendo doc original + extracción fallida + error específico. Máximo 2–3 intentos. Distinguir errores recuperables (formato) de no recuperables (dato ausente en la fuente).
- **⚠ Evita:** Reintentar sin feedback es ruido. Aceptar salida fallida rompe contratos downstream. Reintentar cuando el dato no existe en la fuente garantiza alucinación.
- **Modelo mental:** loop: `extract → validate → si error, extract+feedback → validate`. Max 2–3 intentos. Feedback debe ser el error específico, no un mensaje genérico. Tras N intentos sin éxito: marcar `needs_human_review` con cadena de errores. Recuperable (formato) vs no recuperable (info ausente) son ramas distintas.
- **GOOD:** `def extract_with_retry(client,doc,schema,max_retries=2): last_error=None; for attempt in range(max_retries+1): feedback=f"Intento previo falló: {last_error}\nOutput previo: {extraction}\nCorrige SOLO lo que el error señala." if last_error else ""; resp=create(tools=[schema],tool_choice=...,messages=[{doc+feedback}]); try: validate(extraction,schema); return {...,"attempts":attempt+1} except ValidationError as e: last_error=str(e); return {...,"needs_human_review":True}`.
- **✗ ANTI:** `for _ in range(5): ext=...; try: validate(ext); return ext except: continue # mismo prompt, sin feedback` + aceptar salida fallida en silencio.
- **✓ argumento:** distinguir error recuperable de no recuperable; describir el loop con feedback específico; identificar patrones sistemáticos para fix estructural; escalar con cadena de errores cuando max_retries se agota.
- **quiz:** C·B·C (P1: error no recuperable -dato no existe en fuente, marcar needs_human_review; P2: reemplazar por retry-with-error-feedback específico; P3: `detected_pattern` sistemático -80% del mismo error → ajustar schema/prompt o normalizar en post-process, no subir retries).

### Kata 27 · Multi-Pass Review e Independent Reviewer
- **slug:** `katas-independent-reviewer-multipass` · **escenarios:** Code Gen, CI/CD
- **Qué es:** El modelo que generó código retiene el contexto de su razonamiento; es mal revisor de su propio output. Una instancia independiente (sesión nueva, sin la cadena de generación) detecta más issues. Para PRs grandes: multi-pass per-file + cross-file integration.
- **⚠ Evita:** Self-review produce reviews superficiales o auto-justificativas: feedback inconsistente, bugs obvios omitidos. Single-pass sobre 14 archivos dispersa atención. 'Consensuar 2 de 3 reviews' suprime issues raros legítimos.
- **Modelo mental:** self-review: misma sesión, contexto sesgado, ineficaz. Independent reviewer: sesión limpia, ve solo el código resultante. Pass A: per-file deep dive. Pass B: cross-file integration. Quorum 2-de-3 NO es solución: filtra issues raros legítimos.
- **GOOD:** `def review_pr(client,files): per_file=[review_file_independent(client,path,content) for path,content in files.items()]; summary=json.dumps(per_file); return create(system="Detecta interacciones cross-file y duplicados de findings.",messages=[summary])`. `review_file_independent` usa SESIÓN NUEVA (reviewer no vio la generación).
- **✗ ANTI:** self-review en la misma sesión (`resp_gen` → "Ahora revisa lo que escribiste") + quorum 2-de-3 que descarta señal genuina.
- **✓ argumento:** enunciar por qué self-review es subóptimo; separar per-file de cross-file pass; argumentar contra quorum N-de-M; asegurar sesiones limpias para reviewers independientes.
- **quiz:** B·B·B (P1: el quorum filtra señal genuina rara, no compensa contexto sesgado; P2: reviewer independiente -sesión limpia, solo ve el código resultante; P3: Pass A per-file deep dive + Pass B cross-file integration).

### Kata 29 · Confidence Calibration y Stratified Sampling
- **slug:** `katas-confidence-stratified-sampling` · **escenarios:** Multi-Agent, Structured Extraction
- **Qué es:** Para extracciones masivas, el modelo emite field-level confidence scores. Esos scores se CALIBRAN contra un labeled validation set (la confianza raw está sesgada). Calibrados, enrutan trabajo: high confidence → auto + stratified sampling; low → revisión humana. Medir accuracy por document_type y field, nunca agregada.
- **⚠ Evita:** Reportar '97% accuracy global' y automatizar todo lo high-confidence suena seguro hasta que un tipo de doc falla en silencio. Stratified sampling es la red que detecta nuevos modos de error que un validation set viejo no captura.
- **Modelo mental:** confidence raw != probabilidad real de correctitud. Calibración: comparar score vs accuracy empírica por bucket en validation set. Stratified sampling: proporcional por document_type y rango de score. Agregate accuracy miente; reportar desglosada.
- **GOOD:** `EXTRACT_WITH_CONF` schema con `field_confidence:{type:number,min:0,max:1}` required. `calibrate(predictions,labeled_set)` → buckets por thresh comparando pred vs truth. `stratified_sample(extractions,n_per_type=10)` muestrea high-confidence por doc_type. Routing por accuracy empírica.
- **✗ ANTI:** `if extraction["field_confidence"]>=0.9: return "auto" # confía ciegamente, sin calibrar` + `print(f"Accuracy: {global_acc}") # 97% que oculta 60% en un segmento`.
- **✓ argumento:** diferenciar confianza raw de calibrada; describir stratified sampling y por qué supera al random; rechazar reportar accuracy agregada; conectar calibración con routing operativo (auto vs human).
- **quiz:** B·B·B (P1: NO automatizar sin calibración, comparar contra labeled validation por bucket; P2: accuracy desglosada por document_type y field; P3: stratified sampling muestreando bucket high-confidence, detecta drift en segmentos minoritarios).

### Kata 30 · Criterios Explícitos para Reducir Falsos Positivos
- **slug:** `katas-false-positive-criteria` · **escenarios:** Customer Support, CI/CD, Structured Extraction
- **Qué es:** Instrucciones vagas ('be conservative','only high-confidence') fallan: el modelo las interpreta distinto cada vez. Los criterios categóricos con ejemplos positivos y negativos por nivel de severidad producen clasificación consistente. Un alto FP rate en UNA categoría destruye confianza en TODAS; deshabilitar la problemática temporalmente.
- **⚠ Evita:** Si el reviewer reporta 'potential security issue' en código seguro 1 de 5 veces, los devs ignoran TODOS los flags de seguridad, incluso los reales. La precisión es prerrequisito de la utilidad. La confianza es cross-categoría.
- **Modelo mental:** 'confidence' como filtro no funciona: el modelo está mal calibrado. Criterios categóricos: 'reporta solo cuando X claim pero código hace Y', no 'reporta inconsistencias'. Severidad con ejemplos de código positivo y negativo. Si una categoría arrastra FPs, deshabilitarla mientras se afina; preservar la confianza global.
- **GOOD:** `SYSTEM_EXPLICIT`: "Reporta findings SOLO si cumplen UNO de estos criterios: - security.hardcoded_secret: literal API key en código. Positivo: `OPENAI_KEY='sk-abc...'`. Negativo: `OPENAI_KEY=os.environ['OPENAI_KEY']`. - bug.null_deref: dereferencia un value sin chequeo cuando puede ser None. NO reportes: estilo, patterns 'que podrían ser problemáticos'. Severidad: error (rompe runtime), warning (degrada edge case)."
- **✗ ANTI:** `SYSTEM_VAGUE="Eres reviewer. Reporta findings de alta confianza. Sé conservador con los flags."` — interpretado distinto cada turno.
- **✓ argumento:** reescribir prompts vagos en categóricos con ejemplos positivos y negativos; medir FP rate POR CATEGORÍA, no agregada; usar disable temporal de categorías problemáticas para preservar confianza cross-categoría; argumentar por qué 'confidence' como filtro no funciona.
- **quiz:** B·C·B (P1: 'conservative' es subjetivo, ejemplos por categoría dan clasificación estable; P2: deshabilitar la categoría problemática mientras se afina, preserva confianza global; P3: 'reporta solo cuando el comentario claim X pero el código hace Y', con ejemplos positivo y negativo).

---

## D5 · Context & Reliability

### Kata 10 · Prefix caching
- **slug:** `katas-prefix-caching` · **escenarios:** Customer Support, Dev Productivity
- **Qué es:** La API de Claude reusa el cache KV cuando el prefijo del prompt es idéntico turno a turno; organizando el contexto como estático primero y dinámico al final, el primer ~90% del prompt entra en cache y se factura ~10% del costo.
- **⚠ Evita:** Insertar la fecha actual o un `user_id` al inicio del prompt invalida el cache en cada llamada; mismo contenido, 10x más caro, sin que el log lo evidencie.
- **Modelo mental:** estático = system prompt, CLAUDE.md, tool definitions, contexto pesado del repo. Dinámico = input del usuario, timestamps, estado efímero del turno. Regla: estático arriba, dinámico abajo; el borde dinámico se aísla con tags XML (`<reminder>`). Métrica: `cache_creation_input_tokens` vs `cache_read_input_tokens` en usage.
- **GOOD:** `messages=[{system:SYSTEM_PROMPT_BIG_AND_STABLE},{user:REPO_CONTEXT_BIG},prior_turns,{user:f"<reminder>now: {now}</reminder>\n{user_input}"}]; create(system=[{type:"text",text:SYSTEM_PROMPT_BIG_AND_STABLE,cache_control:{type:"ephemeral"}}],...)`.
- **✗ ANTI:** `system_content=f"Today is {datetime.now()}..."+SYSTEM_PROMPT` — fecha al inicio invalida cache cada llamada.
- **✓ argumento:** la regla 'estático-prefix-first, dynamic-suffix-last' y saber interpretar `cache_creation_input_tokens` vs `cache_read_input_tokens` para estimar el ahorro (~10x).
- **quiz:** B·B·B (P1: valor dinámico -timestamp,user_id al inicio rompe el prefix caching; P2: cambiar UN carácter invalida desde ese punto en adelante; P3: dato dinámico -hora al final, en tag `<reminder>` aislado).

### Kata 11 · Mitigación de Dilución Softmax (Edge Placement + Compactación)
- **slug:** `katas-context-dilution-mitigation` · **escenarios:** Multi-Agent Orchestration
- **Qué es:** La curva de atención del transformer tiene forma de U: bordes (inicio/fin) reciben atención alta, el centro se diluye (lost in the middle). Las reglas críticas se colocan en los bordes del prompt, y al pasar ~50% del contexto se compacta antes de perderlas.
- **⚠ Evita:** Un agente puede seguir una política al turno 5 y violarla al turno 30 sin haberla olvidado: solo dejó de atenderla porque quedó en el medio. La pérdida es silenciosa, no aparece en logs ni errores visibles.
- **Modelo mental:** bordes = atención alta. Centro = atención baja (curva en U). Reglas críticas (seguridad, compliance) van al inicio Y se repiten al final como `<reminder>`; los datos ricos van al centro. Si `usage_fraction(history)>0.55`, compactar: reescribir denso preservando reglas, decisiones y escaladas (no borrar).
- **GOOD:** `SYSTEM:<rules>critical_policy</rules>` ... `USER:question` ... `REMINDER:<rules>critical_policy</rules>` + `if usage_fraction(history)>0.55: history=compact(history,preserve=['rules','decisions','escalations'])`.
- **✗ ANTI:** `system_prompt=f"You are an assistant.\n{big_blob_of_context}\nIMPORTANT: never expose PII.\n...3000 more tokens..."` — regla crítica enterrada en el valle de la U.
- **✓ argumento:** describir la curva U de atención y el efecto 'lost in the middle'; enunciar la regla 'bordes para reglas críticas, centro para datos' y fijar un umbral concreto de compactación (50–60%) justificando el balance entre conservar contexto y evitar dilución.
- **quiz:** B·C·B (P1: la regla quedó en el centro y la atención se diluyó, solución repetirla en borde final como reminder + compactar; P2: reglas críticas, decisiones tomadas y escaladas se preservan al compactar; P3: repetir la misma regla al inicio Y al final cubre el riesgo de dilución -ambas son zonas de atención alta).

### Kata 12 · Prompt Chaining Multi-Pass
- **slug:** `katas-multipass-prompt-chaining` · **escenarios:** Multi-Agent Orchestration
- **Qué es:** Cuando una tarea no cabe cognitivamente (auditar 50 archivos, resumir 200 páginas), se descompone en pases secuenciales: pase local por unidad con salida tipada, y luego pase de integración que solo ve los resúmenes, no las unidades crudas.
- **⚠ Evita:** Pedir 'audita estos 50 archivos' en un solo prompt satura la atención del modelo: pierde detalles, alucina entre archivos y produce un resumen genérico. Encadenar mantiene cada pase enfocado, barato y verificable, y permite paralelizar el pase 1.
- **Modelo mental:** Pase 1 (paralelo): por unidad, salida tipada y compacta según schema. Pase 2 (integración): solo ve los outputs del pase 1, no las unidades crudas; nunca ve la totalidad sin filtrar. Cada pase tiene schema declarado y el siguiente consume esos schemas; los pases se componen como una pipeline.
- **GOOD:** `# Pase 1: por archivo, schema FileFindings\nlocal=[analyze_file(f,schema=FileFindings) for f in files]\n# Pase 2: integración solo sobre resúmenes tipados\nreport=integrate(local,schema=AuditReport)`.
- **✗ ANTI:** `mega_prompt='\n\n'.join(open(f).read() for f in files); create(messages=[{user:f'Audita todo:\n{mega_prompt}'}])` — satura atención (Kata 11), no paraleliza.
- **✓ argumento:** identificar tareas candidatas para chaining versus single-pass; diseñar schemas de transición entre pases; conectar con Kata 4 (subagentes para paralelizar el pase 1) y Kata 11 (cada pase respeta límite de contexto).
- **quiz:** B·A·A (P1: chaining con schemas tipados, pase 2 nunca ve los originales; P2: NO conviene cuando la tarea cabe holgadamente y el overhead de coordinación supera el beneficio; P3: sin estado de error tipado por unidad, el pase 2 cree que tiene N-1 unidades válidas, falla silenciosa).

### Kata 18 · Scratchpad Persistente
- **slug:** `katas-persistent-scratchpad` · **escenarios:** Developer Productivity
- **Qué es:** Un archivo (`investigation-scratchpad.md`) externo a la conversación donde el agente vuelca descubrimientos durables: hipótesis confirmadas, decisiones, hallazgos de archivos, pendientes. Sobrevive a `/compact` y a reinicios de sesión.
- **⚠ Evita:** Cuando el contexto se compacta (Kata 11), se pierde detalle. Si un descubrimiento crítico vivía solo en el historial conversacional, desaparece. El scratchpad es memoria persistente curada por el propio agente que sobrevive a cualquier reset.
- **Modelo mental:** conversación = memoria volátil (puede compactarse o resetearse). Scratchpad = memoria persistente en disco. El agente escribe solo conclusiones validadas (Hipótesis, Decisiones, Hallazgos, Pendientes), no monólogo interno. Al inicio de cada sesión el agente lee el scratchpad una vez; después referencia en lugar de re-leer (preserva cache, Kata 10).
- **GOOD:** `# Investigation Scratchpad\n## Decisiones\n- 2026-04-25: usar pydantic v2 (T-19 confirmó compat).\n## Hallazgos\n- src/legacy/parser.py bug offset línea 142 (replicado).\n## Pendientes\n- Verificar si --strict rompe tests integration` + `def append_scratchpad(section,entry): ...`.
- **✗ ANTI:** confiar en la conversación como memoria a largo plazo (tras /compact el hallazgo desaparece) o scratchpad sin estructura / re-leído cada turno (rompe cache).
- **✓ argumento:** describir la diferencia entre memoria conversacional (volátil) y persistente (scratchpad); enunciar qué se escribe y qué no; conectar con Kata 11 (compactación) y Kata 19 (investigación adaptativa).
- **quiz:** B·C·B (P1: persistir hallazgos en scratchpad estructurado en disco y leerlo al reanudar; P2: NO va al scratchpad el monólogo interno / hipótesis no confirmadas / dudas pasajeras; P3: leer scratchpad una vez al inicio y referenciar/anexar después, no re-leer cada turno).

### Kata 20 · Preservación de Provenance
- **slug:** `katas-provenance-preservation` · **escenarios:** Multi-Agent Orchestration, Structured Extraction
- **Qué es:** Cada afirmación factual extraída de fuentes mantiene un mapeo tipado a su origen: `claim, source_id, source_name, publication_date`. Los conflictos entre fuentes NO se resuelven en silencio: se marcan con `conflict=true` y se enrutan a humano.
- **⚠ Evita:** Tras agregar contenido de muchas fuentes vía subagentes (Kata 4), perder el hilo de 'quién dijo qué' hace imposible auditar el resultado. Resúmenes en prosa libre se ven correctos y alucinan sin que se note. Provenance tipada es la única defensa.
- **Modelo mental:** no hay claim sin source: es un invariante de schema. Si dos fuentes contradicen, se registran ambas bajo `conflict=true`; no se promedia, no se elige. La fecha de publicación importa pero no decide: el humano necesita verla para juzgar (fuente más reciente no siempre gana).
- **GOOD:** `claims=[{"claim":"ARR Q3 2025 = 12M USD","sources":[{"id":"doc-A","name":"Annual Report","date":"2025-12-01"},{"id":"doc-B","name":"Investor Deck","date":"2025-09-15"}],"conflict":False},{"claim":"Headcount end-2025","sources":[{"id":"doc-A","value":"450"},{"id":"doc-C","value":"462"}],"conflict":True,"needs_human_review":True}]`.
- **✗ ANTI:** `summary="La empresa tiene ARR de 12M USD y 462 empleados..."` — sin source_id, sin fecha, sin conflicto marcado.
- **✓ argumento:** enunciar el invariante 'no hay claim sin source'; describir la política de conflictos (registrar ambos, no promediar, escalar vía Kata 16); conectar con Kata 4 (agregación tras subagentes paralelos) y Kata 15 (verificación numérica).
- **quiz:** C·B·B (P1: provenance preserva ambas posturas, marca conflicto y escala -humano juzga; P2: invariante 'no hay claim sin source con id y fecha'; P3: test estructural que asserta `each claim_in_output has a non-empty sources[] field con source_id existente`).

---

## Apéndice A · Mapa escenario → kata (oficial)

- **API Integration Reliability:** 06
- **CI/CD:** 26, 27, 30
- **CI/CD Automation:** 13, 17
- **Code Audit Pipeline:** 04
- **Code Gen:** 07, 08, 09, 23, 24, 25, 27
- **Code Generation:** 19
- **Customer Support:** 01, 02, 03, 05, 06, 10, 15, 16, 21, 22, 25, 28
- **Dev Productivity / Developer Productivity:** 07, 08, 09, 10, 18, 19, 21, 22, 23, 24, 25
- **Financial Compliance:** 02
- **Legacy ERP Integration:** 03
- **Multi-Agent / Orchestration:** 01, 04, 11, 12, 19, 20, 21, 28, 29
- **Structured Extraction:** 05, 14, 15, 17, 20, 26, 29, 30

## Apéndice B · Clave de respuestas (quiz oficial)

| Kata | Respuestas | Kata | Respuestas | Kata | Respuestas |
|---|---|---|---|---|---|
| 01 | B·B·B | 11 | B·C·B | 21 | B·B·C |
| 02 | B·C·B | 12 | B·A·A | 22 | B·C·C |
| 03 | C·B·B | 13 | B·C·B | 23 | C·C·B |
| 04 | B·B·B | 14 | B·B·B | 24 | B·B·C |
| 05 | B·B·B | 15 | C·B·B | 25 | B·C·B |
| 06 | B·B·B | 16 | B·B·B | 26 | C·B·C |
| 07 | B·B·B | 17 | B·B·B | 27 | B·B·B |
| 08 | B·B·B | 18 | B·C·B | 28 | B·B·C |
| 09 | B·B·B | 19 | C·B·B | 29 | B·B·B |
| 10 | B·B·B | 20 | C·B·B | 30 | B·C·B |
