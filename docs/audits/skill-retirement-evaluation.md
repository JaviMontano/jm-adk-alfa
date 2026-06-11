# Skill Retirement Evaluation — jm-adk-alfa → Pristino Beta

**Fecha:** 2026-06-11 · **Base:** main @ 563e2bc6 (tag `alfa-final`) · **Autor:** evaluación asistida, evidencia regenerada por script

## Resumen ejecutivo

Alfa carga 611 skills (61MB; 3.5MB solo en SKILL.md). El costo de contexto al inicio de sesión es: Claude Code ~14K tokens, Antigravity ~35-40K (`.agent/skills_index.json` = 133KB), Codex ~20K. `[CÓDIGO]`

Solo **270 skills son load-bearing** (referenciados desde `agents/`, `commands/`, `prompts/`, `hooks/`); **341 no tienen ninguna referencia**. `[CÓDIGO: migrate/build-refs.py, ver docs/audits/coverage-matrix.csv]`

Decisión: **alfa se congela como archivo histórico** (tag `alfa-final`). La funcionalidad load-bearing migra a **Pristino Beta**, un repo nuevo catalog-driven con ~92 skills (routers parametrizados + librería compartida), agents 261→~30, commands 267→~50.

## Evidencia

| Hallazgo | Evidencia | Tag |
|---|---|---|
| 611 skills, 61MB | `ls skills \| wc -l`, `du -sh skills` | `[CÓDIGO]` |
| Ledger: 152 dod-complete / 445 pending | `docs/audits/skill-review-ledger.csv` (597 filas) | `[DOC]` |
| 445 pending sin commits desde import masivo 2026-05-30 | `git log` por skill | `[CÓDIGO]` |
| 270 load-bearing / 341 sin referencias | `docs/audits/coverage-matrix.csv` (regenerado por script, no estimado) | `[CÓDIGO]` |
| 10 pares duplicados confirmados | input-analysis/input-analyst, context-optimizer/context-optimization, discovery-orchestrator/discovery-orchestration, accessibility-audit/accessibility-testing, firebase-auth/firebase-auth-setup, firebase-hosting/firebase-hosting-setup, api-design/api-designer, google-analytics/analytics-implementation, code-review/ai-code-review, state-management/state-management-design | `[CÓDIGO]` |
| Skills genéricos que reescriben conocimiento base del modelo | javascript-patterns, node-development, rest-api-development, testing-fundamentals, component-patterns, database-design, error-handling-patterns | `[INFERENCIA]` |
| Boilerplate por skill ~96KB (SKILL.md + README + 4 agentes triada casi idénticos + knowledge graph + prompts + templates + examples) | inspección de estructura | `[CÓDIGO]` |
| Bug YAML folded-scalar en `.agent/skills_index.json` (descripciones `>` sin resolver) | generate_index.py parsea frontmatter naive | `[CÓDIGO]` |
| Pack jarvis-os (14 skills) NO está en ledger pero es intencional (commit 2026-06-05 "Personal Jarvis OS capability pack") — SE CONSERVA | `git log -- skills/jarvis-os` | `[CÓDIGO]` |

## Disposiciones

| Categoría | Cantidad aprox. | Disposición |
|---|---|---|
| Load-bearing (referenciados) | 270 | Migran a beta: consolidados en ~92 (routers por dominio + 24 competencias standalone + pack jarvis-os) |
| Pares duplicados (mitad perdedora) | 10 | Alias en `catalog/skills.json` de beta |
| Genéricos (conocimiento base) | ~9 | No migran; referencias re-cableadas al router más cercano (reporte scripted) |
| Pending + sin referencias | ~320 | No migran; alfa es el archivo |
| Boilerplate por skill (README, 4 agentes, knowledge/, examples/, prompts/, templates/) | 611× | Sustituido por librería compartida `references/` en beta |
| Constituciones v4.1/v5.2 | 2 | Solo v6.0.0 migra |
| Agentes especialistas 1:1 y stubs de command autogenerados | ~230 agents, ~215 commands | No migran; reemplazados por 4 plantillas de rol parametrizadas + dispatcher |

## Arquitectura destino (beta)

- **Catalog-driven**: `catalog/skills.json` única fuente de verdad; superficies por runtime generadas (patrón spec-kit `CommandRegistrar`/HarnessAdapter).
- **Skill = contrato delgado**: router con `params:`/`routes:` en frontmatter → playbooks `references/<topic>.md`. Carga perezosa: el router ES el índice del cluster.
- **Determinismo**: scripts emiten JSON, templates lo ingieren, prompts solo aportan juicio (trilogía spec-kit). Gates de fase = existencia de artefacto (patrón iikit `check-prerequisites`).
- **Constitución v6.0.0 en modo enforcement** (HALT ante violación de MUST) en fases de ejecución (patrón iikit).
- **Economía de tokens**: contratos de salida comprimidos en subagentes (~60% menos, patrón caveman), adapters generados en registro comprimido, benchmark 3-arm commiteado (nunca cifras sin datos).
- **Presupuesto inicio de sesión objetivo**: CC ~2.6K / AG ~4K / Codex ~2.3K (gate en CI).

## Trazabilidad

`docs/audits/coverage-matrix.csv`: 611 filas, una por skill alfa. Columnas `disposition`, `beta_home`, `rationale` se completan desde `consolidation-map.yaml` en beta; el gate de CI de beta (`validate-coverage.py`) exige cero filas sin disposición explícita antes de declarar paridad funcional.

---
*Sin precios. Esfuerzo estimado del refactor: 8-12 días-persona.* `[INFERENCIA]`
