---
name: finops
description: >
  Financial Operations para cloud — visibilidad de costos, optimización, gobernanza, y cultura
  de responsabilidad financiera. Usar cuando el usuario pida "optimizar costos cloud",
  "implementar FinOps", "gobernanza de costos", "cost allocation", "showback/chargeback",
  o mencione FinOps, cloud cost management, reserved instances, savings plans, right-sizing,
  cost anomaly detection, o unit economics para cloud. [EXPLICIT]
model: opus
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
version: 1.0.0
---

# Metodologia FinOps — Cloud Financial Operations

Financial Operations para cloud — visibilidad completa de costos, optimización de rate y usage,
gobernanza financiera, forecasting, y unit economics. Transforma cloud cost de un gasto opaco
en un driver de decisiones de negocio con responsabilidad distribuida por equipos. [EXPLICIT]

---

## Principio Rector

1. **Everyone takes ownership of their cloud usage** — FinOps is a cultural shift, not just a tooling exercise. Engineers, finance, and leadership share accountability for cloud spend. Sin ownership distribuido, la optimización es un juego de whack-a-mole centralizado. [EXPLICIT]

2. **Decisions are driven by business value, not just cost reduction** — a $10K/month service that generates $100K revenue is well-spent. El objetivo no es "gastar menos" sino "gastar mejor". Cost efficiency sin business context es austeridad ciega. [EXPLICIT]

3. **Cloud cost is a variable, manageable expense** — real-time data enables real-time decisions. A diferencia de infraestructura on-premise (CAPEX fijo), cloud es OPEX variable. Esto es una ventaja competitiva si se gestiona activamente; un riesgo financiero si se ignora. [EXPLICIT]

---

## Inputs

```
Parametros:
  MODO:         [piloto-auto | desatendido | supervisado | paso-a-paso]
  PROFUNDIDAD:  [express | standard | deep]
  FORMATO:      [ejecutivo | tecnico | hibrido]
  CLOUD:        [aws | azure | gcp | multi-cloud]
  ALCANCE:      [visibility | optimization | governance | full]

Modos de autonomia:
  - piloto-auto: Auto para analisis y recomendaciones, HITL para decisiones de compra (RI/SP). [EXPLICIT]
  - desatendido: Cero interrupciones. Analisis completo con supuestos documentados. [EXPLICIT]
  - supervisado: Autonomo con checkpoint en compras comprometidas y cambios de gobernanza. [EXPLICIT]
  - paso-a-paso: Confirma cada seccion, cada recomendacion, y cada calculo. [EXPLICIT]

Deteccion automatica:
  - Si existe billing data o Cost Explorer → CLOUD se infiere del provider
  - Si el input menciona "RI" o "savings plans" → ALCANCE incluye optimization
  - Si el input menciona "tags" o "allocation" → ALCANCE incluye visibility
  - Si el input menciona "forecast" o "budget" → ALCANCE incluye governance
  - Default: MODO=piloto-auto, PROFUNDIDAD=standard, ALCANCE=full, CLOUD=aws
```

---

## When to Use

- Implementar programa FinOps desde cero (greenfield)
- Optimizar costos cloud existentes (rate optimization, right-sizing, idle detection)
- Diseñar estrategia de tagging y cost allocation
- Implementar showback/chargeback para equipos o business units
- Crear forecasting y budget management para cloud spend
- Calcular unit economics (cost per transaction, cost per user, cloud P&L)
- Evaluar madurez FinOps y definir roadmap de mejora (Crawl/Walk/Run)
- Detectar anomalias de costo y establecer alertas

## When NOT to Use

- Auditar arquitectura AWS especifica para AI → **metodologia-aws-architecture-audit**
- Diseñar arquitectura cloud nueva → **metodologia-aws-architecture-design**
- Implementar infraestructura cloud → **metodologia-aws-architecture-implementation**
- Migrar workloads a cloud → **metodologia-cloud-migration**
- Estimar costos de un proyecto nuevo → **metodologia-cost-estimation**
- Analisis financiero horizontal (no cloud) → **metodologia-analisis-horizontal-financiero**

---

## Delivery Structure: 6 Sections

### S1: Cost Visibility & Allocation

Establece la base de visibilidad: saber quien gasta que, donde, y por que. [EXPLICIT]

```
Load references:
  Read ${CLAUDE_SKILL_DIR}/references/finops-unit-economics.md
```

**Tagging Strategy:**
- Mandatory tags: `Environment`, `Team`, `Project`, `CostCenter`, `Application`, `Owner`
- Optional tags: `Compliance`, `DataClassification`, `ExpirationDate`
- Tag enforcement: SCPs (AWS), Azure Policy, Org Policies (GCP)
- Tag compliance target: >95% de recursos taggeados

**Cost Allocation:**
- Shared cost distribution: proportional, fixed, even-split
- Amortized vs. unblended costs
- Custom allocation rules para shared services (networking, security, platform)

**Dashboards:**
- Daily cost trend por team/project/environment
- Top 10 cost drivers (servicios, cuentas, regiones)
- Tag compliance dashboard
- Anomaly detection alerts

**Entregable:** Tagging strategy document, cost allocation model, dashboard specifications.

### S2: Rate Optimization

Reducir el precio unitario de los recursos cloud sin cambiar el consumo. [EXPLICIT]

```
Load references:
  Read ${CLAUDE_SKILL_DIR}/references/finops-optimization-playbook.md
```

**Reserved Instances / Savings Plans:**
- Coverage analysis: % de usage estable cubierto por commitments
- Target coverage: 70-80% de baseline steady-state
- RI vs. SP decision matrix (flexibility vs. discount depth)
- Term selection: 1yr vs. 3yr (risk vs. savings)
- Payment option: All Upfront > Partial Upfront > No Upfront

**Spot / Preemptible:**
- Workloads elegibles: batch, CI/CD, dev/test, stateless processing
- Interruption handling strategy
- Spot savings estimation

**Enterprise Discounts:**
- EDP/MACC negotiation leverage points
- Committed spend tiers
- Private pricing agreements

**Entregable:** Rate optimization plan con savings estimados por tecnica, timeline de implementacion.

### S3: Usage Optimization

Reducir el consumo eliminando waste y ajustando el tamaño de los recursos. [EXPLICIT]

```
Load references:
  Read ${CLAUDE_SKILL_DIR}/references/finops-optimization-playbook.md
```

**Right-Sizing:**
- CPU utilization <40% sustained → downsizing candidate
- Memory utilization <30% sustained → downsizing candidate
- GPU utilization <50% sustained → evaluate CPU alternative
- Right-sizing cadence: mensual para compute, quarterly para databases

**Idle Resource Detection:**
- Unattached EBS volumes, unused Elastic IPs, idle load balancers
- Dev/test environments running 24/7 (target: 10h/day × 5 days = 30% savings)
- Idle endpoints (SageMaker, API Gateway con zero traffic)

**Scheduling:**
- Non-production environments: auto-stop nights/weekends
- Batch workloads: schedule durante off-peak pricing windows
- Expected savings: 60-70% en non-production compute

**Storage Tiering:**
- S3 lifecycle policies: Standard → IA → Glacier → Deep Archive
- EBS gp3 vs. gp2 migration (20% savings, better performance)
- Snapshot retention policies

**Entregable:** Waste inventory, right-sizing recommendations, scheduling plan, estimated savings.

### S4: FinOps Operating Model

Estructura organizacional, procesos, y cadencia para sostener FinOps. [EXPLICIT]

```
Load references:
  Read ${CLAUDE_SKILL_DIR}/references/finops-operating-model.md
```

**Team Structure:**
- FinOps Lead / Cloud Economist (central)
- Finance Partner (central)
- Engineering Champions (embedded per team)
- Executive Sponsor (C-level)

**Cadence:**
- Daily: automated anomaly alerts, cost dashboards review
- Weekly: team-level cost review (15 min standup)
- Monthly: cross-team optimization review, RI/SP coverage check
- Quarterly: business review, forecast update, maturity assessment

**Maturity Model — Crawl/Walk/Run:**

| Dimension | Crawl | Walk | Run |
|-----------|-------|------|-----|
| Visibility | Basic tagging, monthly reports | Full allocation, daily dashboards | Real-time, automated anomaly detection |
| Optimization | Ad-hoc right-sizing | Systematic RI/SP, scheduling | Autonomous optimization, ML-driven |
| Governance | Reactive budgets | Proactive forecasting | Predictive, business-aligned KPIs |
| Culture | Centralized FinOps team | Team-level champions | Engineering-owned, self-service |

**Entregable:** FinOps operating model document, RACI, cadence calendar, maturity assessment.

### S5: Forecasting & Budgeting

Predecir y controlar el gasto cloud con precision creciente. [EXPLICIT]

**Forecasting Methods:**
- Trend-based: historical extrapolation (± seasonal adjustment)
- Driver-based: cost = f(users, transactions, data volume)
- Bottom-up: team budgets aggregated
- Target accuracy: ±10% (Crawl), ±5% (Walk), ±3% (Run)

**Budget Management:**
- Budget = forecast + buffer (10-15%)
- Alert thresholds: 50%, 75%, 90%, 100%, 110%
- Escalation path per threshold
- Reforecast cadence: monthly (Crawl), bi-weekly (Walk), weekly (Run)

**Anomaly Detection:**
- Baseline: rolling 30-day average per service/account
- Alert trigger: >20% deviation from baseline
- Root cause analysis: new deployment, traffic spike, config change, pricing change
- Response SLA: investigate within 4 hours for >$1K anomalies

**Variance Analysis:**
- Budget vs. Actual vs. Forecast (monthly)
- Variance decomposition: rate change, usage change, scope change
- Trend analysis: MoM, QoQ growth rate

**Entregable:** Forecast model, budget framework, anomaly detection rules, variance report template.

### S6: Unit Economics & Business Alignment

Conectar cloud cost con metricas de negocio para decisiones informadas. [EXPLICIT]

```
Load references:
  Read ${CLAUDE_SKILL_DIR}/references/finops-unit-economics.md
```

**Unit Cost Metrics:**
- Cost per transaction (CPT)
- Cost per active user (CPAU)
- Cost per API call
- Cost per GB processed/stored
- Infrastructure cost as % of revenue

**Margin Analysis:**
- Gross margin impact of cloud cost
- Cloud cost per product line
- Customer-level profitability including infra
- Break-even analysis per feature/service

**Cloud P&L:**
- Revenue attribution per cloud workload
- Direct vs. indirect cloud costs
- Shared services allocation
- Cloud ROI per business initiative

**Showback/Chargeback:**
- Showback: visibility sin billing impact (Crawl/Walk)
- Chargeback: actual cost transfer to business units (Run)
- Allocation model: direct attribution + proportional shared costs
- Billing cadence: monthly with T+5 reconciliation

**Entregable:** Unit economics dashboard, cloud P&L, showback/chargeback model, business alignment scorecard.

---

## Trade-off Matrix

| Profundidad | Scope | Depth | Effort | When to Use |
|------------|-------|-------|--------|-------------|
| **Express** | Visibility + quick wins | Top-line analysis | 2-3 dias | Quick cost review, executive briefing |
| **Standard** | All 6 sections | Full analysis | 5-8 dias | FinOps program launch, quarterly review |
| **Deep** | All 6 + implementation guides | Full + tooling setup | 10-15 dias | Enterprise FinOps transformation |

---

## Assumptions

1. Acceso a billing data (Cost Explorer, billing console, o export)
2. Al menos 3 meses de historico de costos para analisis significativo
3. Tagging parcial existente (si no hay, S1 toma prioridad critica)
4. Stakeholders de engineering y finance disponibles
5. Cloud provider principal identificado (multi-cloud aumenta complejidad)

## Limits

1. NO ejecuta compras de RI/SP — recomienda y el usuario decide/ejecuta
2. NO modifica infraestructura — identifica oportunidades (ver skills de implementation)
3. NO reemplaza Cost Explorer o herramientas nativas — las complementa con metodologia
4. NO provee consejo financiero regulado — es operational efficiency, no investment advice
5. NO audita seguridad ni compliance — solo cost implications (ver skills de audit)

---

## Edge Cases

1. **Startup sin historico**: Usar industry benchmarks y driver-based forecasting. Establecer tagging desde dia 1. Focus en S1 y S4 antes de optimizar. [EXPLICIT]

2. **Multi-cloud environment**: Normalizar costos cross-provider. Usar herramientas multi-cloud (CloudHealth, Apptio, Spot.io). Allocation model debe ser provider-agnostic. [EXPLICIT]

3. **Acquired company integration**: Mapear tagging strategies, unificar cost centers, reconciliar contratos de RI/SP, consolidar billing accounts. [EXPLICIT]

4. **Massive AI/ML spend**: AI workloads tienen patrones unicos (GPU burst, training vs. inference). Separar AI cost center. Evaluar Inferentia/Trainium, spot para training. [EXPLICIT]

5. **Regulated industry**: Cost data puede contener metadata sensible. Chargeback reports deben cumplir data governance. Shared cost allocation debe ser auditable. [EXPLICIT]

## Manejo de Inputs Ambiguos

- Si el cloud provider no se especifica: asumir AWS (default), confirmar si multi-cloud.
- Si el MODO no se especifica: usar `piloto-auto` (default).
- Si la PROFUNDIDAD no se indica: usar `standard` (default).
- Si el ALCANCE no se indica: usar `full` (default). Si el contexto menciona solo "costos" → visibility + optimization. Si menciona "FinOps program" → full.
- Si no hay billing data disponible: documentar como blocker, producir framework teorico basado en arquitectura conocida.
- Si el historico es <3 meses: advertir sobre precision limitada en forecasting, usar benchmarks de industria.

---

## Validation Gate

*El agente que ejecuta este skill debe verificar cada item antes de entregar el output al usuario.*

- [ ] Tagging strategy definida con tags mandatorios y enforcement mechanism
- [ ] Cost allocation model documentado (direct, shared, amortized)
- [ ] Rate optimization analizado: RI/SP coverage, spot eligibility, enterprise discounts
- [ ] Usage optimization: right-sizing, idle detection, scheduling, storage tiering
- [ ] FinOps operating model: roles, RACI, cadence, maturity assessment
- [ ] Forecasting model seleccionado con target accuracy
- [ ] Budget framework con thresholds y escalation paths
- [ ] Anomaly detection rules definidas con response SLA
- [ ] Unit economics calculados (CPT, CPAU, cost as % revenue)
- [ ] Showback/chargeback model definido segun madurez
- [ ] Savings estimados cuantificados por categoria (rate, usage, waste)
- [ ] Roadmap priorizado con quick wins vs. strategic initiatives

---

## Cross-References

| Skill | Relacion |
|-------|----------|
| `aws-architecture-design` | Diseño AWS con cost considerations integradas |
| `aws-architecture-audit` | Auditoría que incluye cost optimization pillar |
| `infrastructure-architecture` | Infraestructura cloud donde se aplica FinOps |
| `cloud-migration` | Migracion cloud donde FinOps debe integrarse desde dia 1 |
| `cost-estimation` | Estimacion de costos para proyectos nuevos |
| `analisis-horizontal-financiero` | Analisis financiero complementario (no cloud) |

---

## Output Format Protocol

```
if FORMATO == "ejecutivo":
  Executive dashboard: total spend, trend, savings opportunities, unit economics
  Audiencia: CFO, CTO, VP Engineering

if FORMATO == "tecnico":
  Full 6-section analysis + implementation details + tool configurations
  Audiencia: Cloud engineers, FinOps practitioners, DevOps

if FORMATO == "hibrido":
  Executive summary + technical deep-dive por seccion
  Audiencia: Engineering managers, technical leads reporting to C-level
```

## Output Artifact

```
## {Organization Name} — FinOps Assessment & Roadmap

### Executive Summary
[Total cloud spend, trend, savings potential, maturity score, top recommendations]

### S1: Cost Visibility & Allocation [Tag Compliance: X%]
[Tagging strategy, allocation model, dashboard specs]

### S2: Rate Optimization [Potential Savings: $XX,XXX/month]
[RI/SP analysis, spot opportunities, enterprise discounts]

### S3: Usage Optimization [Waste Identified: $XX,XXX/month]
[Right-sizing, idle resources, scheduling, storage tiering]

### S4: FinOps Operating Model [Maturity: Crawl|Walk|Run]
[Team structure, RACI, cadence, maturity roadmap]

### S5: Forecasting & Budgeting [Forecast Accuracy: ±X%]
[Forecast model, budget framework, anomaly detection]

### S6: Unit Economics [CPT: $X.XX, Cloud/Revenue: X%]
[Unit costs, margin analysis, cloud P&L, showback/chargeback]

### Implementation Roadmap
[Phased plan with quick wins, medium-term, strategic initiatives]

### Appendix: Savings Detail
[Line-item savings by category with confidence level]
```

---
**Fuente**: FinOps Foundation. *FinOps Framework* (2024). | Storment, J.R. & Fuller, M. (2023). *Cloud FinOps* (2nd ed.). O'Reilly.
