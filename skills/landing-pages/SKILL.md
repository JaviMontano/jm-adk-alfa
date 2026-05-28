---
name: landing-pages
description: >
  Triggers on "landing page", "personal brand page", "portfolio site", "create my web page",
  "página web personal", "create my website", "professional web presence". Creates personal
  brand landing pages and professional web presence pages — dark-first, bilingual ES/EN,
  JM Labs brand system. Output: full self-contained HTML file.
  Argument: person name + page type + optional brief/context.
argument-hint: "person-name [portfolio|consultant|speaker|executive|product] [context]"
model: opus
context: fork
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch
version: 1.0.0
---

# Landing Pages — Personal Brand Web Presence

> TL;DR: Build a high-quality personal brand or professional landing page — dark-first design, bilingual ES/EN, JM Labs brand system, self-contained HTML ready to deploy.

**Principio Rector:** A landing page is a first impression compressed into 5 seconds. Design for clarity, credibility, and a single action.

---

## When to Activate

**Activate when:**
- User says "landing page", "personal brand page", "portfolio site", "create my web page"
- User says "página web personal", "quiero una web", "professional website for me"
- User needs an online presence for job search, consulting, speaking, or freelancing [INFERRED]
- User needs a product or service launch page [EXPLICIT]

**Do NOT activate when:**
- User needs a full multi-page website (redirect to full web design process)
- User needs an e-commerce store (use ecommerce-frontend skill)
- User needs a blog/CMS (use blog-cms skill)
- User needs a marketing funnel with A/B testing (use conversion-optimization skill)

---

## S1 — Page Types

Identify the page archetype before designing. Each has a different content hierarchy. [EXPLICIT]

### Portfolio Page
**For:** Designers, developers, writers, creatives
**Hero:** Name + role + one strong visual or project thumbnail
**Core sections:** Featured projects with outcomes, tech/skill stack, brief bio
**Primary CTA:** "View my work" / "Hire me" / contact form

### Consultant / Freelancer Page
**For:** Independent consultants, coaches, fractional executives
**Hero:** Name + value proposition + credibility signal (clients or results)
**Core sections:** Services, process (how you work), case studies/testimonials, about, contact
**Primary CTA:** "Book a call" / "Get a proposal"

### Speaker / Thought Leader Page
**For:** Keynote speakers, podcast guests, conference presenters
**Hero:** Name + speaking topic + video reel link or thumbnail
**Core sections:** Topics/talks, past events, media kit download, testimonials, contact booking
**Primary CTA:** "Book me to speak" / "Download media kit"

### Executive / Professional Page
**For:** Job seekers, C-suite candidates, board members
**Hero:** Name + current role + professional photo placeholder
**Core sections:** Career highlights (3-5 achievements), expertise areas, education, contact
**Primary CTA:** "Download CV" / "Connect on LinkedIn"

### Product / Service Launch Page
**For:** SaaS products, courses, events, service launches
**Hero:** Product name + one-line value prop + primary CTA above fold
**Core sections:** Problem, solution, features, pricing/tiers, FAQ, social proof
**Primary CTA:** "Start free trial" / "Join waitlist" / "Buy now"

---

## S2 — Content Architecture

Universal content hierarchy that works across all page types. [EXPLICIT]

### Section Map

```
[1] HERO           — Name/product + role/tagline + primary CTA + credibility signal
[2] ABOUT / VALUE  — Who are you? What problem do you solve? Why you?
[3] SERVICES/WORK  — What you offer or what you have built (portfolio/features)
[4] SOCIAL PROOF   — Testimonials, logos, metrics, awards, media mentions
[5] PROCESS / FAQ  — How you work or common questions
[6] CTA BLOCK      — Repeated CTA with urgency or low-friction offer
[7] CONTACT        — Contact form or direct email/calendar link
[8] FOOTER         — Links, legal, social profiles
```

### Copywriting Principles

**Hero Headline Formula:**
`[Result they want] + [for whom] + [without their pain]`

Example: "Strategic product clarity for ambitious startups — without the 6-month consulting engagement."

**Value Proposition Hierarchy:**
1. Primary headline (8 words or fewer, outcome-focused)
2. Subheadline (1-2 sentences, who + how + proof)
3. Supporting bullets (3 max, each starting with a benefit verb)
4. CTA button (action verb + specificity: "Book your free 30-min call")

**Social Proof Formats (ranked by trust level):**
1. Video testimonial with name + role + company
2. Quote + name + role + company + photo
3. Logo grid (logos of companies you worked with)
4. Specific metric ("Helped 47 companies raise Series A")
5. Media mention ("As featured in...")

---

## S3 — JM Labs HTML System

Full implementation spec for the HTML page. [EXPLICIT]

### Brand Tokens

```css
:root {
  /* Core brand palette */
  --jml-navy:    #122562;   /* primary background sections */
  --jml-gold:    #FFD700;   /* accent, CTAs, highlights */
  --jml-blue:    #137DC5;   /* links, secondary actions, icons */
  --jml-bg:      #0d1b3e;   /* page background (darkest) */
  --jml-surface: rgba(255,255,255,0.05); /* card background */
  --jml-border:  rgba(255,215,0,0.2);   /* gold-tinted borders */

  /* Typography */
  --font-head: 'Poppins', sans-serif;   /* headings: weight 600-900 */
  --font-body: 'Inter', sans-serif;     /* body: weight 400-800 */

  /* Spacing scale */
  --space-xs: 0.5rem;
  --space-sm: 1rem;
  --space-md: 2rem;
  --space-lg: 4rem;
  --space-xl: 8rem;
}
```

### CSS Classes Reference

| Class | Usage |
|-------|-------|
| `.jml-doc` | Root wrapper for all JM Labs pages |
| `.slide` | Full-viewport hero section |
| `.bridge` | Transitional summary section (navy bg, centered) |
| `.cta` | Call-to-action block with gold button |
| `.mv` | Main value section (content sections) |
| `.ml` | Multi-layout section (2-3 column grids) |
| `.gold` | Gold text accent class |
| `.src` | Evidence chip (explicit/inferred/open) |

### Bilingual Pattern (ES/EN)

```html
<!-- Language toggle button -->
<button class="lang-toggle gold" onclick="toggleLang()">ES | EN</button>

<!-- Bilingual content — show/hide via JS -->
<h1>
  <span data-l="es">Tu Nombre Aqui</span>
  <span data-l="en" style="display:none">Your Name Here</span>
</h1>

<script>
  let lang = 'es';
  function toggleLang() {
    lang = lang === 'es' ? 'en' : 'es';
    document.querySelectorAll('[data-l]').forEach(el => {
      el.style.display = el.dataset.l === lang ? '' : 'none';
    });
  }
</script>
```

### Dark/Light Mode Toggle

```css
[data-theme="light"] {
  --jml-bg: #f0f4ff;
  --jml-navy: #e8eeff;
  --jml-surface: rgba(18,37,98,0.05);
  color: #122562;
}
```

```html
<button class="theme-toggle"
  onclick="document.documentElement.dataset.theme =
    document.documentElement.dataset.theme === 'light' ? '' : 'light'">
  Dark / Light
</button>
```

### Full HTML Page Template Structure

```html
<!DOCTYPE html>
<html lang="es" data-theme="">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Name] — [Tagline]</title>
  <!-- SEO + OG meta tags (see S4) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;900&family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
  <style>/* All CSS inline — fully self-contained */</style>
</head>
<body>
  <nav><!-- Minimal: name/logo + lang toggle + theme toggle --></nav>
  <main>
    <section class="slide" id="hero">    <!-- [1] Hero --></section>
    <section class="bridge" id="about">  <!-- [2] About --></section>
    <section class="mv" id="services">   <!-- [3] Services/Work --></section>
    <section class="ml" id="proof">      <!-- [4] Social Proof --></section>
    <section class="mv" id="process">    <!-- [5] Process/FAQ --></section>
    <section class="cta" id="cta">       <!-- [6] CTA Block --></section>
    <section class="mv" id="contact">    <!-- [7] Contact --></section>
  </main>
  <footer><!-- Social links + legal --></footer>
  <script>/* Lang toggle + theme toggle + smooth scroll */</script>
</body>
</html>
```

---

## S4 — SEO & Performance

Target Lighthouse 95+ on Performance, Accessibility, and SEO. [EXPLICIT]

### Meta Tags

```html
<!-- Basic SEO -->
<title>[Name] — [Role] | [City]</title>
<meta name="description" content="[1-2 sentence value proposition. 150 chars max.]">
<link rel="canonical" href="https://[yourdomain.com]/">

<!-- Open Graph (social sharing) -->
<meta property="og:title" content="[Name] — [Role]">
<meta property="og:description" content="[Same as meta description]">
<meta property="og:image" content="https://[domain]/og-image.png">
<meta property="og:url" content="https://[yourdomain.com]">
<meta property="og:type" content="website">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="[Name] — [Role]">
<meta name="twitter:image" content="https://[domain]/og-image.png">

<!-- Schema.org Person markup -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "[Full Name]",
  "jobTitle": "[Title]",
  "url": "https://[domain]",
  "sameAs": ["https://linkedin.com/in/...", "https://twitter.com/..."]
}
</script>
```

### Performance Rules

- All fonts via Google Fonts with `display=swap` (prevents FOIT) [EXPLICIT]
- No external CSS/JS beyond Google Fonts — fully self-contained file [EXPLICIT]
- Hero section: text + CSS gradient background (no large images above fold) [EXPLICIT]
- Images: use WebP format, explicit width/height attributes (prevents CLS) [EXPLICIT]
- CSS: minified inline, no render-blocking resources [EXPLICIT]
- Contact form: HTML5 native form action (Formspree URL) — no JS libraries [EXPLICIT]

---

## S5 — Deploy Options

Three paths from simple to robust. [EXPLICIT]

### Option A: Hostinger (Recommended for non-devs)
1. Export HTML as `index.html`
2. Upload via Hostinger File Manager to `public_html/`
3. Configure custom domain in DNS panel
4. Enable free SSL in control panel
**Cost:** $3-10/month [EXPLICIT]

### Option B: Firebase Hosting (Recommended for devs)
```bash
npm install -g firebase-tools
firebase login
firebase init hosting
firebase deploy
```
Free SSL, global CDN, custom domain supported. [EXPLICIT]
**Cost:** Free on Spark plan for static pages [EXPLICIT]

### Option C: GitHub Pages (Completely free)
1. Create repo `username.github.io`
2. Push `index.html` to main branch
3. Enable Pages in repo Settings → Pages → Deploy from branch
4. Add CNAME file for custom domain
**Cost:** Free [EXPLICIT]

---

## Trade-off Matrix

| Mode | Time | Output | Best For |
|------|------|--------|---------|
| **Quick** (1h) | Fast | Hero + contact section only | Job applications, LinkedIn supplement |
| **Standard** (3h) | Medium | Full 7-section page, bilingual | Consultant/freelancer launch |
| **Premium** (6h) | Slow | Full page + animations + SEO schema + deploy guide | Executive brand, speaker page |

---

## Assumptions & Limits

- Single-page only (no routing, no CMS, no database) [EXPLICIT]
- User provides content brief or answers content prompts [EXPLICIT]
- No real images included — CSS placeholder divs with aspect ratios provided [EXPLICIT]
- Google Fonts CDN required (offline font embedding increases file size significantly) [EXPLICIT]
- Contact form submissions require Formspree or similar (backend not included) [EXPLICIT]
- This skill generates HTML/CSS/JS code — deployment is the user's action [EXPLICIT]

---

## Edge Cases

| Scenario | Handling |
|----------|---------|
| User has no photo for hero | CSS-based avatar with initials in gold circle on navy bg |
| User wants animation-heavy page | CSS keyframe animations only — no external libraries (self-contained rule) |
| User content is only in English | Skip bilingual toggle, single-language version |
| User needs WCAG accessibility | Add aria-labels, alt text, focus indicators, skip-nav link |
| User wants both dark and light as default | Default to dark; light toggle available; document in code comments |

---

## Good vs Bad Example

**BAD hero section:**
> "Welcome to my website. I am a professional with many years of experience."

**GOOD hero section:**
> Headline: "I help Series A startups find product-market fit." | Subheadline: "Product strategist with 11 years in B2B SaaS. Former Head of Product at Rappi." | CTA button: "Book a free discovery call"

---

## Validation Gate

- [ ] Page type identified and content architecture matches the archetype (S1)
- [ ] All 7 standard sections present (hero through contact)
- [ ] Hero headline follows outcome + audience + pain-relief formula
- [ ] At least one social proof element included
- [ ] JM Labs brand tokens applied (navy `#122562`, gold `#FFD700`, blue `#137DC5`)
- [ ] Bilingual ES/EN toggle implemented with `data-l` pattern
- [ ] Dark/light mode toggle implemented with `data-theme`
- [ ] All SEO meta tags present (title, description, OG, Twitter Card)
- [ ] Schema.org Person or Product markup included
- [ ] HTML file is fully self-contained (no external CSS/JS beyond Google Fonts)
- [ ] Lighthouse Performance target 95+ achievable (no render-blocking, no large images)

---

## Reference Files

- `knowledge/body-of-knowledge.md` — Web design and conversion psychology foundations
- `evals/` — Scored landing page examples

---

## Related Skills

- `cv-enhancement` — Generate the downloadable CV to link from the executive page
- `seo-architecture` — Deeper SEO strategy for content-rich pages
- `b2b-outreach` — Use the landing page as a credibility asset in outreach messages
- `html-brand` — Lower-level JM Labs HTML brand system reference
