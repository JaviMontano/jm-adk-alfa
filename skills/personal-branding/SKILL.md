---
name: personal-branding
description: >
  Triggers on "personal brand", "brand strategy for me", "how to position myself", "marca personal".
  Builds a complete personal brand strategy including positioning, narrative architecture, platform
  selection, visual identity guidelines, and content pillars. Output: brand strategy document
  plus action plan in markdown. [EXPLICIT]
argument-hint: "professional context, target audience, career goals, current positioning"
model: opus
context: fork
allowed-tools: Read, Write, Edit, Glob, Grep
version: 1.0.0
---

# Personal Branding

> TL;DR — Transforms raw professional context into a structured personal brand strategy covering
> positioning statement, narrative architecture, platform selection, visual identity guidelines,
> and content pillars. Delivers a ready-to-execute brand strategy document with 90-day action plan.

---

## When to Activate

| Signal | Example |
|--------|---------|
| Explicit trigger phrase | "I need a personal brand strategy" |
| Positioning request | "How should I position myself as a data leader?" |
| Spanish variant | "Ayudame con mi marca personal" |
| Career pivot framing | "I'm transitioning into consulting, need branding" |
| Visibility goal | "I want to be known for AI governance" |

Activate when the user seeks structured guidance on professional identity, reputation building,
or thought-leadership positioning. Do NOT activate for corporate brand or product branding
requests — those belong to `brand-voice` or `commercial-model`.

---

## S1 — Discovery & Audit

Before building, extract the raw material:

1. **Professional inventory** — roles held, industries, certifications, signature projects.
2. **Unique value intersection** — where experience, skills, and passion overlap (ikigai lens).
3. **Current digital footprint** — LinkedIn, GitHub, portfolio, publications, speaking history.
4. **Audience definition** — who needs to find and trust this person (hiring managers, clients,
   investors, peers).
5. **Competitor scan** — 3-5 professionals in the same niche; identify gaps and white space.

Output: Discovery Brief (markdown table with findings per dimension).

---

## S2 — Positioning & Narrative Architecture

Build the strategic core:

1. **Positioning statement** — For [audience], [name] is the [category] who [differentiator]
   because [proof points]. Maximum 2 sentences.
2. **Brand promise** — one line describing the transformation the audience receives.
3. **Narrative arc** — Origin (where you started), Turning point (insight or pivot),
   Mission (where you are heading). Three paragraphs, each 40-60 words.
4. **Brand attributes** — 5 adjectives that define tone and personality.
5. **Elevator pitch** — 30-second and 60-second versions, bilingual ES/EN.

Ensure the positioning avoids generic superlatives ("passionate leader") and anchors on
measurable differentiators.

---

## S3 — Platform Strategy & Visual Identity

Map presence to platforms and define visual coherence:

### Platform Selection Matrix

| Platform | Purpose | Frequency | Content Type | Priority |
|----------|---------|-----------|--------------|----------|
| LinkedIn | Authority & network | 3x/week | Articles, carousels | P0 |
| Twitter/X | Real-time thought leadership | Daily | Threads, commentary | P1 |
| Personal site | Portfolio & long-form | Monthly | Case studies | P1 |
| GitHub | Technical proof | As needed | Repos, contributions | P2 |
| Speaking | Credibility amplifier | Quarterly | Talks, panels | P2 |

Adapt the matrix to the user's context — not every professional needs every platform.

### Visual Identity Guidelines

- **Color palette** — primary navy (#122562), accent gold (#FFD700), secondary blue (#137DC5).
- **Typography** — headings in Poppins 600, body in Inter 400. Minimum 16px base.
- **Photography** — professional headshot with neutral or brand-colored background.
- **Templates** — consistent banner dimensions across platforms (1584x396 LinkedIn, 1500x500 X).
- **Dark-first design** — all assets optimized for dark backgrounds first, light variant second.

---

## S4 — Content Pillars & Action Plan

### Content Pillars (3-5)

Each pillar maps to a facet of expertise:

| Pillar | Topic cluster | Audience need | Format mix |
|--------|--------------|---------------|------------|
| P1 | Core expertise | "Teach me" | How-tos, frameworks |
| P2 | Industry perspective | "Inform me" | Commentary, analysis |
| P3 | Personal journey | "Inspire me" | Stories, lessons learned |
| P4 | Curated insights | "Save me time" | Digests, tool reviews |

### 90-Day Action Plan

- **Days 1-7** — Finalize positioning statement, update headshot, rewrite LinkedIn headline.
- **Days 8-14** — Build content backlog (8 posts minimum), set up scheduling tool.
- **Days 15-30** — Publish 3x/week on primary platform; engage 15 min/day.
- **Days 31-60** — Launch secondary platform; repurpose top-performing content.
- **Days 61-90** — Measure metrics (impressions, followers, inbound leads); iterate pillars.

---

## Trade-off Matrix

| Decision | Option A | Option B | Recommendation |
|----------|----------|----------|----------------|
| Platform breadth | All platforms at once | Sequential rollout | Sequential — depth beats breadth |
| Tone | Strictly professional | Personal + professional | Blend — authenticity drives engagement |
| Frequency | Daily posting | 3x/week quality posts | 3x/week — consistency over volume |
| Visual investment | DIY Canva templates | Professional designer | DIY first, invest after traction |
| Language | English only | Bilingual ES/EN | Bilingual if audience spans both markets |

---

## Assumptions & Limits

- Assumes the user provides honest self-assessment; the skill does not verify claims. [EXPLICIT]
- Does not create visual assets (logos, banners) — delivers specifications only. [EXPLICIT]
- Platform algorithms change frequently; recommendations are based on current best practices. [INFERRED]
- ROI timelines (90 days) assume consistent execution; results vary by niche saturation. [INFERRED]
- Does not manage social media accounts or schedule posts. [EXPLICIT]

---

## Edge Cases

1. **Career pivoter with no public presence** — Start from scratch with a "launch sequence":
   bio-first approach, 10 foundational posts before going active.
2. **Executive with confidentiality constraints** — Avoid naming employers or projects;
   use anonymized case patterns and industry-level insights.
3. **Multilingual professional (3+ languages)** — Define primary and secondary content
   languages; do not spread thin across all languages simultaneously.
4. **User provides minimal input** — Ask structured clarifying questions before proceeding;
   never fabricate professional history.

---

## Good vs Bad Example

### Good

```markdown
## Positioning Statement
For CTOs evaluating cloud migration, Ana Ruiz is the solutions architect
who reduces migration risk by 40% through her proprietary assessment
framework, proven across 12 enterprise migrations in financial services.
```

Why it works: specific audience, quantified differentiator, credible proof.

### Bad

```markdown
## Positioning Statement
Ana is a passionate technology leader who helps companies succeed
with innovative solutions and cutting-edge technology.
```

Why it fails: generic adjectives, no audience, no measurable claim, no proof.

---

## Validation Gate

Before delivering the final brand strategy, confirm every item:

- [ ] Positioning statement is two sentences or fewer with a named audience
- [ ] Narrative arc has three distinct sections (origin, turning point, mission)
- [ ] Platform matrix includes at least 3 platforms with frequency and content type
- [ ] Visual identity references brand colors (#122562, #FFD700, #137DC5) and typography
- [ ] Content pillars number between 3 and 5 with defined audience need per pillar
- [ ] 90-day action plan has weekly or biweekly milestones
- [ ] Elevator pitch exists in both ES and EN versions
- [ ] No fabricated credentials or unverified claims in the output
- [ ] Edge cases documented when user context triggers them
- [ ] Output uses dark-first design tokens where visual specs are provided

---

## Reference Files

| File | Purpose |
|------|---------|
| `references/positioning-frameworks.md` | Positioning statement templates and examples |
| `references/platform-benchmarks.md` | Platform-specific metrics and best practices |
| `references/content-calendar-template.md` | Weekly content planning template |
| `references/brand-audit-checklist.md` | Pre-strategy audit questionnaire |
