---
name: linkedin-optimization
description: >
  Triggers on "optimize my LinkedIn", "LinkedIn profile", "improve my LinkedIn", "mejorar LinkedIn".
  Rewrites LinkedIn profile sections using proven frameworks — headline, about, experience,
  skills, and content plan for SSI improvement. Output: optimized profile text plus content
  calendar in markdown. [EXPLICIT]
argument-hint: "current LinkedIn profile text or URL, target role, industry, career goals"
model: opus
context: fork
allowed-tools: Read, Write, Edit, Glob, Grep
version: 1.0.0
---

# LinkedIn Optimization

> TL;DR — Takes a professional's current LinkedIn profile (or raw career data) and produces
> fully rewritten profile sections using hook-story-offer, PAR bullets, and keyword-rich copy.
> Includes a 30-day content calendar designed to improve Social Selling Index (SSI).

---

## When to Activate

| Signal | Example |
|--------|---------|
| Direct optimization request | "Help me optimize my LinkedIn profile" |
| Section-specific ask | "Rewrite my LinkedIn about section" |
| Spanish variant | "Quiero mejorar mi perfil de LinkedIn" |
| Job search context | "I'm job hunting, fix my LinkedIn" |
| SSI or visibility goal | "How do I increase my LinkedIn SSI score?" |

Activate when the user wants to improve their LinkedIn presence. Do NOT activate for general
social media strategy (use `personal-branding`) or for company LinkedIn pages (use `b2b-outreach`).

---

## S1 — Profile Audit & Keyword Research

### Audit Checklist

Score each dimension 1-5 before rewriting:

| Dimension | Weight | Audit Question |
|-----------|--------|---------------|
| Headline | 25% | Does it state value proposition, not just title? |
| About | 25% | Does it follow hook-story-offer? |
| Experience | 20% | Are bullets achievement-based with metrics? |
| Skills | 10% | Are top 3 skills aligned with target role? |
| Visual | 10% | Professional photo, custom banner, consistent branding? |
| Activity | 10% | Regular posts, comments, article shares? |

### Keyword Extraction

1. Identify 10-15 target keywords from job descriptions in the user's desired role.
2. Map keywords to profile sections (headline: 2-3, about: 5-7, experience: 3-5 per role).
3. Use natural integration — never keyword-stuff.

---

## S2 — Section-by-Section Rewrite

### Headline (220 characters max)

Formula: `[Role] | [Value Proposition] | [Keyword] | [Proof or CTA]`

Example: `Solutions Architect | Reducing cloud migration risk for FinTech | AWS & Azure | 12 enterprise migrations`

Avoid: job title alone ("Software Engineer at Acme Corp").

### About Section (2,600 characters max)

Use the **Hook-Story-Offer** framework:

1. **Hook** (lines 1-2, visible before "see more") — A bold statement or question that stops
   the scroll. Must create curiosity or state a contrarian insight.
2. **Story** (lines 3-12) — Professional narrative with a turning point. Include 2-3 metrics.
   Write in first person. Show personality.
3. **Offer** (lines 13-18) — What you do for your audience. Clear CTA (contact, follow,
   visit portfolio). Include relevant keywords naturally.

### Experience Bullets — PAR Method

Each role gets 3-5 bullets following **Problem-Action-Result**:

```
- Identified $2M annual waste in legacy infrastructure (Problem),
  designed and led migration to serverless architecture (Action),
  reducing operating costs by 47% within 6 months (Result).
```

Rules:
- Start with a strong action verb (Led, Designed, Reduced, Built, Launched).
- Include at least one metric per bullet (%, $, time saved, scale).
- Prioritize recency — most detailed bullets on last 2-3 roles.

### Skills & Endorsements Strategy

1. Pin top 3 skills that match target role keywords.
2. Remove irrelevant or outdated skills (e.g., "Microsoft Word" for a CTO).
3. Endorsement campaign — identify 10 colleagues to request endorsements from; reciprocate.

---

## S3 — Visual & Profile Completeness

### Visual Identity Alignment

- **Profile photo** — professional headshot, face occupies 60%+ of frame, brand-colored
  background or neutral. Resolution: 400x400 minimum.
- **Banner image** — 1584x396px. Include: name/title, value proposition, brand colors
  (navy #122562, gold #FFD700, blue #137DC5). Dark-first design.
- **Typography on banner** — Poppins 600 for name, Inter 400 for tagline.

### Completeness Targets

| Element | Status Target |
|---------|--------------|
| Custom URL | `/in/firstname-lastname` |
| Location | City + open to remote/relocation |
| Creator mode | ON with 5 hashtags aligned to pillars |
| Featured section | 3-5 items: top post, portfolio, case study |
| Recommendations | Minimum 3 given and 3 received |
| Certifications | All relevant certs listed with dates |

---

## S4 — Content Calendar & SSI Improvement

### 30-Day Content Calendar

| Week | Mon | Wed | Fri |
|------|-----|-----|-----|
| W1 | Industry insight (text) | Carousel: framework | Comment sprint (10) |
| W2 | Personal story + lesson | Poll: audience question | Share + commentary |
| W3 | How-to post (step list) | Carousel: case study | Comment sprint (10) |
| W4 | Contrarian take | Video: 60s tip | Weekly roundup |

### SSI Score Levers

The Social Selling Index has 4 pillars (each 0-25, total 0-100):

| SSI Pillar | Actions to Improve |
|------------|-------------------|
| Establish professional brand | Complete profile, publish long-form content |
| Find the right people | Use Sales Navigator, connect with ICP |
| Engage with insights | Comment meaningfully on 5+ posts/day |
| Build relationships | Send personalized connection requests, nurture DMs |

Target: SSI above 70 within 60 days of consistent activity.

---

## Trade-off Matrix

| Decision | Option A | Option B | Recommendation |
|----------|----------|----------|----------------|
| Headline style | Title-focused | Value-prop focused | Value-prop — 40% more profile views |
| About tone | Formal third person | Conversational first person | First person — higher engagement |
| Content frequency | Daily posting | 3x/week | 3x/week with daily commenting |
| Creator mode | ON | OFF | ON — unlocks follow button and hashtags |
| Open to Work banner | Visible to all | Recruiters only | Recruiters only unless actively unemployed |

---

## Assumptions & Limits

- Assumes the user provides truthful career information; the skill does not verify claims. [EXPLICIT]
- Does not access or scrape LinkedIn directly — works from user-provided text or copy-paste. [EXPLICIT]
- SSI score improvement estimates assume consistent daily activity for 60+ days. [INFERRED]
- Algorithm changes may affect content reach; recommendations follow current patterns. [INFERRED]
- Does not send connection requests, messages, or post on behalf of the user. [EXPLICIT]

---

## Edge Cases

1. **Career changer with mismatched history** — Lead with the About section narrative explaining
   the pivot; reframe past experience bullets to highlight transferable skills.
2. **Executive who cannot share metrics** — Use directional language ("significantly reduced",
   "led a team of 50+") and focus on scope and complexity instead of exact figures.
3. **Non-English primary market** — Write the About section in the target language with an
   English summary paragraph at the end; adapt keyword research to local job market terms.
4. **Student or early-career with no experience** — Emphasize projects, coursework, volunteer
   work, and certifications; use the Featured section to showcase portfolio pieces.

---

## Good vs Bad Example

### Good

```markdown
## Headline
Cloud Solutions Architect | Saving FinTechs $2M+/year through serverless migration
| AWS Certified | Speaker

## About (Hook)
Most cloud migrations fail not because of technology — but because nobody mapped
the business processes first.
```

Why it works: value-led headline with metric, contrarian hook that creates curiosity.

### Bad

```markdown
## Headline
Solutions Architect at Acme Corp

## About
I am a passionate and results-driven professional with 10+ years of experience
in the technology industry. I am looking for new opportunities.
```

Why it fails: title-only headline, generic about with no hook, no story, no offer.

---

## Validation Gate

Before delivering the optimized profile, confirm every item:

- [ ] Headline is 220 characters or fewer and contains a value proposition
- [ ] About section follows hook-story-offer structure with a visible-before-fold hook
- [ ] At least 3 experience entries have PAR-formatted bullets with metrics
- [ ] Top 3 skills are aligned to target role keywords
- [ ] Visual guidelines specify banner dimensions and brand colors (#122562, #FFD700, #137DC5)
- [ ] Content calendar covers at least 4 weeks with 3 posts per week
- [ ] SSI improvement actions are mapped to all 4 pillars
- [ ] Featured section recommendations include at least 3 items
- [ ] Bilingual note included when user's market requires ES/EN
- [ ] No fabricated metrics or unverified claims in rewritten copy

---

## Reference Files

| File | Purpose |
|------|---------|
| `references/hook-story-offer-examples.md` | Proven About section templates |
| `references/par-bullet-library.md` | PAR bullet examples by industry |
| `references/ssi-benchmarks.md` | SSI score benchmarks by industry and role |
| `references/linkedin-algorithm-notes.md` | Current algorithm signals and ranking factors |
