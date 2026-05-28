---
name: progress-tracker
description: >
  Triggers on "seguimiento de avance", "progress report", "status update", "informe de progreso",
  "track milestones", "weekly report", "reporte semanal", "project dashboard", "create progress document".
  Creates branded progress tracking documents — HTML dashboard, XLSX tracker, or markdown report.
  JM Labs dark brand system. Bilingual ES/EN. [EXPLICIT]
argument-hint: "project-name or description of what to track"
model: opus
context: fork
allowed-tools: Read, Write, Edit, Glob, Grep
version: 1.0.0
---

# progress-tracker — Project Progress & Status Reports

> **TL;DR:** Turn any project status into a branded progress document — weekly reports, milestone dashboards, KPI trackers, action item logs. JM Labs dark style · Bilingual ES/EN · Print-ready.

**Principio Rector:** Un documento de seguimiento no es burocracia — es memoria activa. Cada reporte responde tres preguntas: ¿qué hicimos?, ¿estamos en ruta?, ¿qué desbloqueamos mañana?

---

## When to Activate

**Activate when:**
- User asks for "seguimiento", "avance", "progress report", "weekly status"
- A project needs a milestone tracking document
- Stakeholder update is needed (executive brief format)
- Action item log needs to be created or updated
- KPI dashboard for a project or initiative is required

**Do NOT activate when:**
- Request is purely for code analysis (use x-ray-skill)
- Request is for a business proposal (use executive-pitch or jmlabs-corporate-doc)
- Simple one-line status update in chat (no document needed)

**Before generating:** Collect: project name, reporting period, key milestones, responsible parties, status (green/amber/red), blockers, next actions.

---

## S1 — Document Types

| Type | When to use | Output format |
|------|-------------|---------------|
| `--type=weekly` | Regular cadence, 1-page summary | Branded HTML |
| `--type=milestone` | Gate review, delivery checkpoint | Branded HTML with timeline |
| `--type=dashboard` | Executive view, multi-project | Branded HTML with KPI cards |
| `--type=xlsx` | Editable tracker, recurring use | XLSX template scaffold |
| `--type=markdown` | GitHub/internal use | Markdown report |

---

## S2 — Progress Report Structure

### Standard Sections

```
1. Header: Project name · Period · Date · Owner · Status (RAG)
2. TL;DR: 3 bullets — what was done, where we stand, what's next
3. Milestones (table): Name · Target · Actual · Status (🟢🟡🔴) · Owner
4. KPIs (if applicable): Metric · Target · Actual · Trend (↑↓→)
5. Action Items: Item · Owner · Due · Status
6. Risks & Blockers: Item · Severity · Mitigation · Owner
7. Next Period Plan: Top 3-5 priorities
8. Decisions Log: Decision · Date · Made by · Impact
```

### RAG Status Convention

| Color | Meaning | When to use |
|-------|---------|-------------|
| 🟢 Green | On track | Milestones met, no blockers |
| 🟡 Amber | At risk | Minor delays, manageable blockers |
| 🔴 Red | Off track | Critical blocker, missed milestones |

---

## S3 — HTML Dashboard Output

### Branded HTML Shell

```html
<!DOCTYPE html>
<html lang="es" class="dark">
<head>
  <meta charset="UTF-8">
  <title>{PROJECT} — Seguimiento {PERIOD} | JM Labs</title>
  <style>
    :root {
      --navy: #122562; --gold: #FFD700; --blue: #137DC5;
      --bg: #0d1b3e; --card: rgba(255,255,255,.05);
      --text: #E2E8F0; --text-s: #94A3B8; --heading: #fff;
    }
    body { font-family: 'Inter', system-ui, sans-serif; background: var(--bg);
           color: var(--text); margin: 0; padding: 2rem; }
    .jml-header { border-bottom: 2px solid var(--gold); padding-bottom: 1rem; margin-bottom: 2rem; }
    .jml-header h1 { font-family: 'Poppins', sans-serif; color: var(--heading);
                     margin: 0; font-size: clamp(1.5rem, 4vw, 2.5rem); }
    .period { color: var(--gold); font-size: .875rem; margin-top: .25rem; }
    .rag { display: inline-block; padding: .25rem .75rem; border-radius: 999px;
           font-weight: 700; font-size: .875rem; }
    .rag-green { background: rgba(34,197,94,.15); color: #4ade80; }
    .rag-amber { background: rgba(234,179,8,.15); color: #fbbf24; }
    .rag-red   { background: rgba(239,68,68,.15); color: #f87171; }
    .cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px,1fr));
             gap: 1rem; margin: 2rem 0; }
    .card { background: var(--card); border: 1px solid rgba(255,215,0,.15);
            border-radius: .5rem; padding: 1.25rem; }
    .card .mv { font-size: 2rem; font-weight: 800; color: var(--gold); }
    .card .ml { font-size: .75rem; color: var(--text-s); text-transform: uppercase;
                letter-spacing: .05em; margin-top: .25rem; }
    table { width: 100%; border-collapse: collapse; margin: 1rem 0; }
    th { background: rgba(19,125,197,.2); color: var(--blue); padding: .75rem;
         text-align: left; font-size: .8125rem; }
    td { padding: .625rem .75rem; border-bottom: 1px solid rgba(255,255,255,.07);
         font-size: .8125rem; }
    .section-title { color: var(--gold); font-family: 'Poppins', sans-serif;
                     font-weight: 700; font-size: 1.125rem; margin: 2rem 0 .75rem; }
    @media print { body { background: #fff; color: #111; }
                   .card { border-color: #ccc; }
                   .rag-green { color: #166534; } }
  </style>
</head>
<body>
  <div class="jml-header">
    <h1>
      <span data-l="es">{PROYECTO}</span>
      <span data-l="en">{PROJECT}</span>
      &nbsp;—&nbsp;
      <span class="rag rag-{STATUS_CLASS}">
        <span data-l="es">{STATUS_ES}</span>
        <span data-l="en">{STATUS_EN}</span>
      </span>
    </h1>
    <div class="period">
      <span data-l="es">Período: {PERIODO} · Generado: {FECHA}</span>
      <span data-l="en">Period: {PERIOD} · Generated: {DATE}</span>
    </div>
  </div>

  <!-- KPI Cards -->
  <div class="cards">
    <div class="card">
      <div class="mv">{MILESTONES_DONE}/{MILESTONES_TOTAL}</div>
      <div class="ml"><span data-l="es">Hitos completados</span><span data-l="en">Milestones done</span></div>
    </div>
    <div class="card">
      <div class="mv">{ACTIONS_OPEN}</div>
      <div class="ml"><span data-l="es">Acciones abiertas</span><span data-l="en">Open actions</span></div>
    </div>
    <div class="card">
      <div class="mv" style="color:var(--gold)">{BLOCKERS}</div>
      <div class="ml"><span data-l="es">Bloqueantes activos</span><span data-l="en">Active blockers</span></div>
    </div>
  </div>

  <!-- Milestones Table -->
  <div class="section-title">
    <span data-l="es">Hitos del Período</span>
    <span data-l="en">Period Milestones</span>
  </div>
  <table>
    <thead><tr>
      <th><span data-l="es">Hito</span><span data-l="en">Milestone</span></th>
      <th><span data-l="es">Meta</span><span data-l="en">Target</span></th>
      <th><span data-l="es">Real</span><span data-l="en">Actual</span></th>
      <th><span data-l="es">Estado</span><span data-l="en">Status</span></th>
      <th><span data-l="es">Responsable</span><span data-l="en">Owner</span></th>
    </tr></thead>
    <tbody>
      <!-- {MILESTONE_ROWS} -->
    </tbody>
  </table>

  <!-- Action Items -->
  <div class="section-title">
    <span data-l="es">Acciones Pendientes</span>
    <span data-l="en">Pending Actions</span>
  </div>
  <table>
    <thead><tr>
      <th><span data-l="es">Acción</span><span data-l="en">Action</span></th>
      <th><span data-l="es">Responsable</span><span data-l="en">Owner</span></th>
      <th><span data-l="es">Vence</span><span data-l="en">Due</span></th>
      <th><span data-l="es">Estado</span><span data-l="en">Status</span></th>
    </tr></thead>
    <tbody>
      <!-- {ACTION_ROWS} -->
    </tbody>
  </table>

  <script>
    function toggleLang() {
      const h = document.documentElement;
      h.lang = h.lang === 'es' ? 'en' : 'es';
    }
  </script>
</body>
</html>
```

---

## S4 — XLSX Tracker Template

When `--type=xlsx`, output a structured scaffold description for creating an Excel tracker:

```
Sheet 1: Dashboard
  - Project name, period, overall RAG status
  - KPI summary cards (milestone %, actions open, blockers)

Sheet 2: Milestones
  Columns: ID | Milestone | Category | Target Date | Actual Date | Status | Owner | Notes
  Conditional formatting: Green = Done, Amber = At Risk, Red = Overdue

Sheet 3: Action Items
  Columns: ID | Action | Owner | Due Date | Priority | Status | Dependencies | Notes
  Filter by: Owner, Status, Priority

Sheet 4: Risks & Blockers
  Columns: ID | Description | Type | Severity | Probability | Impact | Mitigation | Owner | Status

Sheet 5: Decisions Log
  Columns: Date | Decision | Context | Made By | Impact | Follow-up Required
```

---

## S5 — Markdown Report Format

For internal/GitHub use:

```markdown
# {PROJECT} — Progress Report: {PERIOD}

**Status:** {RAG} | **Owner:** {OWNER} | **Generated:** {DATE}

## TL;DR
- ✅ {WHAT_WAS_DONE}
- 📍 {WHERE_WE_STAND}
- ▶️ {WHATS_NEXT}

## Milestones
| Milestone | Target | Actual | Status | Owner |
|-----------|--------|--------|--------|-------|
| {NAME} | {TARGET} | {ACTUAL} | 🟢/🟡/🔴 | {OWNER} |

## Action Items
| # | Action | Owner | Due | Status |
|---|--------|-------|-----|--------|
| 1 | {ACTION} | {OWNER} | {DUE} | Open/Done |

## Risks & Blockers
| Risk | Severity | Mitigation | Owner |
|------|----------|-----------|-------|
| {RISK} | High/Med/Low | {PLAN} | {OWNER} |

## Next Period Priorities
1. {P1}
2. {P2}
3. {P3}
```

---

## S6 — Data Gathering Protocol

When user provides minimal input, ask for:

```
1. Project name and brief description
2. Reporting period (e.g., Week 12, Q1 2026, Sprint 3)
3. Milestones planned for this period — and which are done/in-progress/blocked
4. Open action items with owners and due dates
5. Key blockers (if any)
6. Top 3 priorities for next period
7. Any decisions made this period
```

If user pastes unstructured notes, extract the above automatically and confirm before generating.

---

## Trade-off Matrix

| Decision | Enables | Constrains | When to use |
|----------|---------|------------|-------------|
| HTML dashboard | Visual, branded, shareable link | Not editable as spreadsheet | Stakeholder presentations |
| XLSX tracker | Editable, formula-driven, recurring | Requires Excel/Sheets, no brand | Operations teams, recurring tracking |
| Markdown | Git-friendly, lightweight, versionable | No visual polish | Developer teams, GitHub projects |
| Bilingual ES/EN | International teams | +20% markup | LATAM + US/EU stakeholders |
| Weekly cadence | Regular rhythm, historical record | More work for PM | Active projects |
| Milestone-only | Focused on key checkpoints | Less detail | Executive sponsors |

---

## Assumptions & Limits

- [EXPLICIT] HTML output uses JM Labs brand system (navy `#122562` · gold `#FFD700` · dark-first)
- [EXPLICIT] XLSX output is a structural scaffold — formulas and conditional formatting described but user applies them
- [INFERRED] User provides raw status data; this skill structures and formats it
- [OPEN] Integration with live project management tools (Jira, Linear) — not currently automated; requires API access

---

## Edge Cases

| Scenario | Handling |
|----------|----------|
| No structured data — just verbal update | Extract via structured questions (S6), confirm before generating |
| Multi-project portfolio | Use `--type=dashboard` with separate card per project |
| Retrospective (past period) | Mark as historical, add lessons learned section |
| Executive-only audience | Strip technical details, emphasize business impact and RAG |
| Recurring weekly template | Generate template HTML with `{{PLACEHOLDER}}` variables for reuse |

---

## Good vs Bad Example

**Bad:**
```
Status: things are going ok, some delays, will finish soon
```

**Good (structured output):**
```
Project: MetodologIA Platform | Period: W12 2026 | Status: 🟡 Amber
✅ Done: Design system v2 delivered (3 days early)
⚠️ At risk: API integration blocked — pending vendor credentials (Owner: Javier, ETA: 2026-03-29)
▶️ Next: Complete auth module, unblock staging deployment
```

---

## Validation Gate

- [ ] Document type matches user need (HTML / XLSX / markdown)
- [ ] Project name, period, and date present in header
- [ ] RAG status (🟢🟡🔴) applied to overall project and each milestone
- [ ] Milestones table complete with target, actual, owner
- [ ] Action items table with owner and due date
- [ ] At least 3 "Next Period" priorities listed
- [ ] Bilingual data-l attributes on all visible text (if HTML)
- [ ] JM Labs brand tokens used (no raw hex colors outside CSS variables)
- [ ] Blockers explicitly flagged (not buried in prose)
- [ ] Print styles active if HTML output

---

## Reference Files

| File | Load when |
|------|-----------|
| `references/report-templates.md` | For extended examples: executive dashboard, portfolio view, retrospective format |

**Orchestrated by:** `jmlabs-corporate-doc` — when `--type=report` is used in a full corporate document context.
