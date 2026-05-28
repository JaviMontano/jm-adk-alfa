---
name: bilingual-doc
description: >
  Triggers on "bilingual", "ES/EN toggle", "bilingual document", "dual language",
  "español e inglés", "agregar idioma", "make it bilingual". Implements the JM Labs
  bilingual pattern — [data-l="es"]/[data-l="en"] toggle via html[lang] attribute.
  INDEPENDENT skill but ALWAYS orchestrated by jmlabs-corporate-doc when brand context is active.
argument-hint: "content to bilingualize OR document to add EN/ES toggle"
model: sonnet
context: fork
allowed-tools: Read, Write, Edit, Glob, Grep
version: 1.0.0
---

# bilingual-doc — Bilingual ES/EN Document Pattern

> **TL;DR:** Implement the JM Labs bilingual system — `[data-l]` attributes + `html[lang]` toggle — in any HTML document. Works standalone or when called by `jmlabs-corporate-doc`.

**Principio Rector:** El contenido bilingüe no es traducción — es presentación paralela. El documento existe simultáneamente en ES y EN, y el usuario elige cuál leer. El brand style orquesta cuándo se activa esta skill.

---

## When to Activate

**Activar cuando:**
- El usuario pide "bilingüe", "ES/EN", "en español e inglés"
- El documento va a una audiencia mixta (LATAM + USA/España)
- `jmlabs-corporate-doc` lo invoca con `bilingual=true` [EXPLICIT desde brand-config.json]
- Documento existente sin soporte bilingüe que hay que actualizar

**Modo orquestado (lo normal):**
`jmlabs-corporate-doc` activa `bilingual-doc` automáticamente. No requiere invocación manual del usuario.

**Modo standalone:**
El usuario puede invocar directamente para añadir bilingüismo a cualquier HTML existente.

**NO activar cuando:**
- Documento puramente interno (README, SKILL.md, notas)
- Usuario confirma que audiencia es solo hispana o solo angloparlante
- Documento técnico sin intención de presentación a cliente

---

## S2 — The Bilingual System

### CSS Rules (ya incluidas en corporate-template.css)

```css
/* Default: mostrar español */
[data-l]            { display: none; }
[data-l="es"]       { display: inline; }

/* Con html[lang="en"]: mostrar inglés */
html[lang="en"] [data-l="es"] { display: none; }
html[lang="en"] [data-l="en"] { display: inline; }

/* Variantes block (párrafos, divs) */
[data-lb="es"]      { display: block; }
[data-lb="en"]      { display: none; }
html[lang="en"] [data-lb="es"] { display: none; }
html[lang="en"] [data-lb="en"] { display: block; }
```

### JavaScript Toggle

```javascript
function toggleLang() {
  const h = document.documentElement;
  h.lang = h.lang === 'es' ? 'en' : 'es';
}
```

### HTML Attribute (`lang`) on Root

```html
<!-- Default: español -->
<html lang="es" class="dark">

<!-- Después de toggle: inglés -->
<!-- html[lang="en"] activa las reglas CSS -->
```

---

## S3 — Markup Patterns

### Inline text (mismo párrafo, frases cortas)

```html
<h2>
  <span data-l="es">El problema está en el método</span>
  <span data-l="en">The problem is in the method</span>
</h2>

<p style="font-size:.875rem;">
  <span data-l="es">MetodologIA transforma la forma en que las organizaciones adoptan IA.</span>
  <span data-l="en">MetodologIA transforms how organizations adopt AI.</span>
</p>
```

### Block content (párrafos completos, diferentes estructuras)

```html
<!-- Cuando ES y EN tienen estructura HTML diferente -->
<div data-lb="es">
  <p>Texto en español con <strong>énfasis</strong> en diferentes palabras.</p>
  <ul>
    <li>Punto uno en español</li>
    <li>Punto dos en español</li>
  </ul>
</div>
<div data-lb="en">
  <p>English text with <strong>emphasis</strong> on different words.</p>
  <ul>
    <li>Point one in English</li>
    <li>Point two in English</li>
  </ul>
</div>
```

### Navigation button

```html
<!-- In top nav bar -->
<button class="jml-nav-btn" onclick="toggleLang()" id="lang-btn">ES/EN</button>
```

### Sidebar nav labels

```html
<div class="jml-sidenav">
  <a href="#problem">
    <span class="dot"></span>
    <span class="label">
      <span data-l="es">El Problema</span>
      <span data-l="en">The Problem</span>
    </span>
  </a>
  <a href="#solution">
    <span class="dot"></span>
    <span class="label">
      <span data-l="es">La Solución</span>
      <span data-l="en">The Solution</span>
    </span>
  </a>
</div>
```

### Table of Contents

```html
<a href="#market">
  <span class="num">3</span>
  <span data-l="es">Mercado — 10 verticales</span>
  <span data-l="en">Market — 10 verticals</span>
</a>
```

### Metadata (page title via JS)

```javascript
// Actualizar título del documento al cambiar idioma
function toggleLang() {
  const h = document.documentElement;
  h.lang = h.lang === 'es' ? 'en' : 'es';
  document.title = h.lang === 'es'
    ? '{TITULO_ES} | JM Labs'
    : '{TITLE_EN} | JM Labs';
}
```

---

## S4 — Content Translation Workflow

Cuando el usuario aporta contenido en un solo idioma, seguir este proceso:

### Desde español → añadir inglés

```
1. Identificar todos los nodos de texto visibles en el HTML
2. Para cada nodo:
   - Si es inline: envolver con <span data-l="es">original</span>
     y añadir <span data-l="en">traducción</span>
   - Si es bloque: usar data-lb="es" / data-lb="en"
3. Añadir toggle button al nav
4. Verificar: NO dejar texto "desnudo" (sin data-l) excepto: números, símbolos, marcas
```

### Desde inglés → añadir español

```
Mismo proceso. Español es siempre el default (html lang="es").
```

### Texto que NO necesita data-l

```html
<!-- Números, símbolos, URLs, emails, nombres propios — sin atributo -->
<div class="mv">557</div>        <!-- número -->
<span>JM Labs</span>             <!-- marca -->
<span>©2026</span>               <!-- símbolo -->
contacto@jmlabs.io               <!-- email -->
<span class="src">WEF 2026</span><!-- source chip -->
```

---

## S5 — Edge Cases

### Texto muy largo con estructura diferente en cada idioma

```html
<!-- Usar data-lb en lugar de data-l -->
<div data-lb="es">
  <h3>La metodología que faltaba</h3>
  <p>Durante años, la promesa de la IA fue enorme — pero la realidad decepcionante.
     No era falla de las herramientas, sino del <strong>método</strong>.</p>
</div>
<div data-lb="en">
  <h3>The missing methodology</h3>
  <p>For years, AI's promise was enormous — but reality disappointing.
     Not a tool failure, but a <strong>method</strong> failure.</p>
</div>
```

### Formularios y CTAs

```html
<a href="mailto:contacto@jmlabs.io" class="cta">
  <span data-l="es">Agendar reunión →</span>
  <span data-l="en">Schedule meeting →</span>
</a>

<input placeholder="" data-placeholder-es="Tu nombre" data-placeholder-en="Your name">
<script>
  // Actualizar placeholders al cambiar idioma
  function updatePlaceholders() {
    const lang = document.documentElement.lang;
    document.querySelectorAll('[data-placeholder-es]').forEach(el => {
      el.placeholder = lang === 'es' ? el.dataset.placeholderEs : el.dataset.placeholderEn;
    });
  }
  function toggleLang() {
    const h = document.documentElement;
    h.lang = h.lang === 'es' ? 'en' : 'es';
    updatePlaceholders();
  }
</script>
```

### SEO / hreflang (si el documento va a web pública)

```html
<head>
  <!-- hreflang para SEO bilingüe -->
  <link rel="alternate" hreflang="es" href="{URL}?lang=es">
  <link rel="alternate" hreflang="en" href="{URL}?lang=en">
</head>
```

---

## Validation Gate

- [ ] `html[lang="es"]` como default en el root element
- [ ] Toggle button `ES/EN` en top nav
- [ ] TODOS los textos visibles envueltos en `[data-l]` o `[data-lb]`
- [ ] Textos "desnudos" solo para números, símbolos, marcas y emails
- [ ] Títulos de navegación (sidebar, TOC) también bilingües
- [ ] `document.title` actualizado en `toggleLang()`
- [ ] Sin mezcla: no usar `data-l` en un lugar y texto hardcodeado en otro
- [ ] Validar: activar toggle y verificar que NO quede texto en idioma incorrecto

---

## S7 — Assumptions & Limits

- [EXPLICIT] CSS para bilinguismo incluido en `brand/jmlabs/corporate-template.css`
- [EXPLICIT] Par de idiomas soportados: ES (default) ↔ EN
- [INFERRED] El sistema funciona sin JavaScript para lectura inicial (ES visible por defecto con CSS puro)
- [INFERRED] El toggle es cliente-side; no hay routing de servidor
- [OPEN] Idiomas adicionales (PT, FR) — posible extendiendo el patrón con `data-l="pt"` pero requiere ampliar CSS
- [OPEN] Traducciones — el usuario debe aportar el texto en ambos idiomas; esta skill no traduce automáticamente

---

## Reference Files

| Archivo | Cargar cuando |
|---------|---------------|
| `brand/jmlabs/brand-config.json` | Cuando se orquesta desde jmlabs-corporate-doc (cargado por el orquestador) |
| `references/bilingual-patterns.md` | Para ejemplos complejos: tablas bilingües, slides completos, modales |

**Skill orquestadora:** `jmlabs-corporate-doc` — esta skill es orquestada, no orquestadora.
