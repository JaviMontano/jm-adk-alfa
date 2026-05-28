---
name: jmlabs-corporate-doc
description: >
  Triggers on "create corporate document", "make investor deck", "build partnership prospectus",
  "design executive brief", "branded HTML report", "JM Labs document", "make it brand friendly".
  Produces self-contained branded HTML corporate documents in JM Labs dark style
  (navy #122562 · gold #FFD700 · blue #137DC5 · Poppins + Inter).
  ALWAYS loads brand-config.json before generating. Orchestrates bilingual-doc for ES/EN output.
argument-hint: "document-type: deck | prospectus | brief | report | proposal"
model: opus
context: fork
allowed-tools: Read, Write, Edit, Glob, Grep
version: 1.0.0
---

# jmlabs-corporate-doc — JM Labs Corporate Document Generator

> **TL;DR:** Produce self-contained branded HTML corporate documents (investor decks, prospectuses, executive briefs, reports) in the JM Labs visual identity. Dark mode · Bilingual ES/EN · Slide-based · Print-ready.

**Principio Rector:** El brand style impone el formato. Antes de cualquier documento, leer `brand/jmlabs/brand-config.json`. La skill `bilingual-doc` siempre es orquestada por esta skill cuando el output requiere ES/EN.

---

## When to Activate

**Activar cuando el usuario pida:**
- "Haz el deck", "crea el prospecto", "diseña el brief ejecutivo"
- "Hazlo brand friendly" (adaptar documento existente al JM Labs brand)
- "Informe corporativo", "propuesta branded", "documento para cliente"
- Cualquier documento que represente a JM Labs ante terceros

**Modos disponibles:**
| Flag | Tipo | Secciones estándar |
|------|------|--------------------|
| `--type=deck` | Investor/Partnership Deck | Cover · TL;DR · Problem · Solution · Model · Traction · Team · CTA |
| `--type=prospectus` | Partnership Prospectus | + Partnership Terms · Entry Fee · Equity |
| `--type=brief` | Executive Brief | TL;DR · Context · Ask · Next Steps |
| `--type=report` | Technical Report | Summary · AS-IS · Findings · Recommendations · Roadmap |
| `--type=proposal` | Commercial Proposal | Cover · Problem · Approach · Team · Timeline · Investment |

**NO activar cuando:** El usuario pide un skill de código, análisis interno, README, o documento sin intención de presentarlo a audiencias externas.

**Antes de generar:** Leer `brand/jmlabs/brand-config.json` [EXPLICIT] y `brand/jmlabs/corporate-template.css` [EXPLICIT].

---

## S2 — Brand Loading Protocol

**OBLIGATORIO. Ejecutar siempre en este orden:**

```
1. Read brand/jmlabs/brand-config.json       → cargar tokens y reglas
2. Read brand/jmlabs/corporate-template.css  → cargar clases CSS
3. Si bilingual=true → activar bilingual-doc  → cargar patrones ES/EN
4. Si el usuario aportó contenido existente  → extraer estructura y revestir
5. Generar HTML self-contained (CSS inline o <style> en <head>)
```

**Tokens críticos (desde brand-config.json):**
- `--navy: #122562` · `--gold: #FFD700` · `--blue: #137DC5`
- Font: `Poppins` (headings 600-900) + `Inter` (body 400-800)
- Modo: dark first (`.light` class override)
- Grids: `.g2` `.g3` `.g4` `.g5`

**PROHIBIDO:**
- `#6366F1` (indigo) · `#22D3EE` (cyan) · `#22C55E` (verde)
- Clash Grotesk · Montserrat como heading · `#0F172A` como background

---

## S3 — Document Structure

### HTML Shell (siempre incluir)

```html
<!DOCTYPE html>
<html lang="es" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
  <meta name="color-scheme" content="dark light">
  <title>{DOCUMENT_TITLE} | JM Labs</title>
  <meta name="robots" content="noindex,nofollow">
  <!-- Favicon JM Labs (inline SVG) -->
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,{JML_LOGO_SVG_ENCODED}">
  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800;900&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>/* corporate-template.css content here */</style>
</head>
<body>
  <!-- Sidebar navigation (right) -->
  <!-- Top navbar with: Logo · Doc type · ES/EN toggle · Dark/Light · Print -->
  <!-- .jml-doc wrapper -->
  <!-- Slides: each section is a .slide with id -->
  <!-- Modals for glossary/evidence -->
  <script>/* toggleLang(), toggleTheme(), reveal(), openModal() */</script>
</body>
</html>
```

### Required JavaScript Functions

```javascript
// Language toggle
function toggleLang() {
  const h = document.documentElement;
  h.lang = h.lang === 'es' ? 'en' : 'es';
}

// Theme toggle
function toggleTheme() {
  document.body.classList.toggle('light');
  document.getElementById('theme-btn').textContent =
    document.body.classList.contains('light') ? '☀' : '☾';
}

// Scroll reveal
const observer = new IntersectionObserver(
  entries => entries.forEach(e => { if(e.isIntersecting) e.target.classList.add('visible'); }),
  { threshold: 0.1 }
);
document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

// Modal
function openModal(id) { document.getElementById(id).classList.add('open'); }
function closeModal(el) { el.classList.remove('open'); }
```

---

## S4 — Section Patterns

### Cover Slide
```html
<div class="slide center" id="cover">
  <div style="max-width:40rem;margin:0 auto;">
    <div class="t" style="color:var(--gold);margin-bottom:1.5rem;">
      <span data-l="es">{TIPO_DOC} · Confidencial · {FECHA}</span>
      <span data-l="en">{DOC_TYPE} · Confidential · {DATE}</span>
    </div>
    <h1 class="brand-font" style="font-size:clamp(2rem,5vw,3rem);margin-bottom:.375rem;">
      JM <span class="gold">Labs</span>
    </h1>
    <p style="font-size:.8125rem;color:var(--text-s);margin-bottom:1.5rem;max-width:28rem;margin-left:auto;margin-right:auto;">
      <span data-l="es">{DESCRIPCION_ES}</span>
      <span data-l="en">{DESCRIPTION_EN}</span>
    </p>
    <!-- Metrics 3-grid -->
    <div class="g3" style="max-width:22rem;margin:0 auto 1.25rem;">
      <div style="text-align:center;"><div class="mv">{KPI1}</div><div class="ml">{LABEL1}</div></div>
      <div style="text-align:center;"><div class="mv">{KPI2}</div><div class="ml">{LABEL2}</div></div>
      <div style="text-align:center;"><div class="mv" style="color:var(--gold);">{KPI3}</div><div class="ml">{LABEL3}</div></div>
    </div>
    <span class="slide-num">1</span>
  </div>
</div>
```

### TL;DR Slide
```html
<div class="slide slide-short" id="tldr">
  <div style="max-width:44rem;">
    <div class="t gold" style="margin-bottom:.375rem;">TL;DR</div>
    <h2 style="font-size:clamp(1.25rem,3vw,1.75rem);margin-bottom:.75rem;">
      <span data-l="es">En 30 segundos</span>
      <span data-l="en">In 30 seconds</span>
    </h2>
    <div class="c" style="border-left:3px solid var(--gold);">
      <p style="font-size:.8125rem;color:var(--text-s);line-height:1.7;">
        <span data-l="es">
          <strong style="color:var(--heading);">Qué:</strong> {QUE_ES}<br>
          <strong style="color:var(--heading);">Por qué:</strong> {POR_QUE}<br>
          <strong style="color:var(--gold);">Siguiente paso:</strong> {SIGUIENTE}
        </span>
        <span data-l="en">
          <strong style="color:var(--heading);">What:</strong> {WHAT_IT_IS}<br>
          <strong style="color:var(--heading);">Why:</strong> {WHY}<br>
          <strong style="color:var(--gold);">Next step:</strong> {NEXT}
        </span>
      </p>
    </div>
  </div>
</div>
```

### Bridge (Evidence/Data Card)
```html
<div class="bridge">
  <span class="bridge-d">
    <span data-l="es">Dato:</span><span data-l="en">Data:</span>
  </span>
  {DATO_CONCRETO} <span class="src" onclick="openModal('{MODAL_ID}')">{FUENTE}</span><br>
  <span class="bridge-i">
    <span data-l="es">{IMPLICACION_ES}</span>
    <span data-l="en">{IMPLICATION_EN}</span>
  </span><br>
  <span class="bridge-a">
    <span data-l="es">{ACCION_ES}</span>
    <span data-l="en">{ACTION_EN}</span>
  </span>
</div>
```

### Sidebar Navigation
```html
<div class="jml-sidenav">
  {SECTIONS.map(s => `
  <a href="#${s.id}">
    <span class="dot" ${s.active ? 'style="background:var(--gold);"' : ''}></span>
    <span class="label">
      <span data-l="es">${s.label_es}</span>
      <span data-l="en">${s.label_en}</span>
    </span>
  </a>`)}
</div>
```

---

## S5 — Evidence Tagging in Documents

Todo claim factual en el documento debe llevar evidencia visible:

```html
<!-- Source chip (inline) -->
<span class="src">WEF 2026</span>
<span class="src">CRO Study</span>

<!-- Tooltip for glossary terms -->
<span class="pop" data-tip="Capacidad de operar con IA sin dependencia del consultor.">
  Soberanía Digital
</span>

<!-- Modal para evidencia extensa -->
<button class="info" onclick="openModal('m-evidence')">i</button>
<div class="modal-bg" id="m-evidence" onclick="if(event.target===this)closeModal(this)">
  <div class="modal">
    <button class="modal-x" onclick="closeModal(this.closest('.modal-bg'))">&times;</button>
    <div class="modal-label" style="background:color-mix(in srgb,var(--blue) 12%,transparent);color:var(--blue);">Evidencia</div>
    <h3>{TITULO}</h3>
    <p>{DETALLE_EVIDENCIA}</p>
  </div>
</div>
```

---

## S6 — Document Type Blueprints

### Investor / Partnership Deck (`--type=deck`)
Slides: Cover → TL;DR → TOC → Problem → Solution → Market → Business Model → Traction → Team → Competition → Risks → Partnership Ask → Next Steps

### Executive Brief (`--type=brief`)
Slides: Cover → TL;DR → Context (1) → Problem (1) → Solution (1) → Ask → Next Steps
*No sidebar nav. Max 6 slides. Max 800 words total.*

### Technical Report (`--type=report`)
Slides: Executive Summary → Methodology → AS-IS Analysis → Findings → Recommendations → Roadmap → Appendix
*Sidebar nav. Evidence chips mandatory. Print-optimized.*

---

## S7 — Trade-off Matrix

| Decisión | Habilita | Limita | Cuándo usar |
|----------|----------|--------|-------------|
| Self-contained (CSS inline) | Sin dependencias externas | Archivo más pesado | Enviar por email / sin servidor |
| External CSS link | Mantenimiento centralizado | Requiere servidor | Repositorio con acceso web |
| Dark mode first | Presentación premium | Puede no imprimir bien | Decks digitales |
| Light mode first | Imprimible, formal | Menos visual | Reportes técnicos formales |
| Bilingual ES/EN | Audiencias mixtas | +20% de markup | Clientes internacionales |
| Solo ES | Markup limpio | Limitado a LatAm/España | Clientes locales confirmados |

---

## S8 — Assumptions & Limits

- [EXPLICIT] Brand tokens canónicos: `brand/jmlabs/brand-config.json`
- [EXPLICIT] CSS completo: `brand/jmlabs/corporate-template.css`
- [INFERRED] Dark mode como default — cambiar a `.light` para impresión formal
- [INFERRED] Google Fonts requiere internet — para offline, usar system fonts: `system-ui, sans-serif`
- [OPEN] Contenido del documento — el usuario debe aportar el texto real
- [OPEN] Idiomas adicionales — sistema actual soporta ES/EN; ampliar con data-l="pt" requiere ajuste

---

## S9 — Good vs Bad Example

**Bad (violaciones de brand):**
```html
<!-- WRONG: color incorrecto, fuente incorrecta -->
<h1 style="color:#6366F1;font-family:'Montserrat'">Mi Empresa</h1>
<button style="background:#22C55E">Siguiente</button>
```

**Good (brand compliant):**
```html
<!-- RIGHT: tokens del brand config -->
<h1 class="brand-font" style="color:var(--heading)">JM <span class="gold">Labs</span></h1>
<a class="cta">Siguiente paso →</a>
```

---

## Validation Gate

- [ ] brand-config.json leído antes de generar
- [ ] Colores solo del palette: `#122562` `#FFD700` `#137DC5` `#BBA0CC` y variables CSS
- [ ] Tipografía: Poppins headings + Inter body
- [ ] Bilingüe: `[data-l="es"]` y `[data-l="en"]` en todo texto visible
- [ ] Sidebar nav presente (decks/reports) con todos los section IDs
- [ ] TL;DR en máximo 3 bullets
- [ ] Evidencia con `.src` chips o modales en claims factuales
- [ ] Ghost menu al final con opciones de próximo paso
- [ ] Print styles activos (`@media print`)
- [ ] HTML self-contained válido (no dependencias externas de CSS crítico)

---

## Reference Files

| Archivo | Cargar cuando |
|---------|---------------|
| `brand/jmlabs/brand-config.json` | SIEMPRE — antes de generar |
| `brand/jmlabs/corporate-template.css` | SIEMPRE — CSS canónico completo |
| `references/document-patterns.md` | Para section blueprints detallados y ejemplos de cada tipo |

**Skill orquestada:** `bilingual-doc` — activar automáticamente cuando `bilingual=true` en brand-config.json.
