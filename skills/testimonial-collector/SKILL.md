---
name: testimonial-collector
description: >
  Triggers on "collect testimonials", "client testimonials", "social proof",
  "testimonios de clientes". Client testimonial and social proof collection
  framework with structured questions, permission templates, formatted quotes,
  and display patterns for web/deck/proposal. Output: formatted testimonials +
  usage guidelines. [EXPLICIT]
argument-hint: "client name(s), project context, intended use (web, deck, proposal), language preference"
model: opus
context: fork
allowed-tools: Read, Write, Edit, Glob, Grep
version: 1.0.0
---

# testimonial-collector

## TL;DR

Provides an end-to-end framework for collecting, formatting, and deploying client testimonials as social proof. Generates structured interview questions, permission/release templates (bilingual ES/EN), standardized testimonial formatting (quote + attribution + context), and ready-to-use display patterns for websites, pitch decks, and proposals. Outputs branded HTML testimonial cards and a reusable testimonial bank.

## When to Activate

- User wants to collect or request testimonials from clients.
- User needs to format existing testimonials for professional use.
- User asks for social proof assets for a website, deck, or proposal.
- User mentions "collect testimonials", "client testimonials", "social proof", or "testimonios de clientes".
- Do NOT activate for case study writing (use `case-study-writing`), general client research (use `client-dossier`), or survey design (use `survey-design`).

## Collection Framework

### Question Bank

Structured questions designed to elicit specific, quotable responses. Organized by depth level:

**Level 1 — Quick Wins (email/form)**: problem identification, standout result, recommendation willingness. 3 questions targeting quotable one-liners.

**Level 2 — Detailed Feedback (call/interview)**: before/after walkthrough, surprise factor, quantified impact, pre-engagement concerns, working-style descriptors. 5 questions targeting outcome metrics and emotional endorsements.

**Level 3 — Story Mining (for case studies)**: turning-point moments, stakeholder reactions, counterfactual ("what if you hadn't done this?"). 3 questions targeting narrative arcs for long-form content.

Each question includes a coaching note explaining what type of testimonial content it typically yields.

### Outreach Templates

Pre-written request messages for different channels:

- **Email template**: professional, warm, 150 words max. Includes context reminder ("We worked together on X in Y"), specific ask, estimated time commitment ("5 minutes"), and deadline.
- **LinkedIn message**: shorter variant, 80 words max, conversational tone.
- **WhatsApp/chat**: ultra-brief, 40 words, with link to form or direct questions.
- **Post-project survey**: embedded in project close-out workflow, 3-5 questions max.

All templates bilingual (ES/EN) with language toggle guidance.

## Permission & Release

### Testimonial Release Template

A lightweight legal-adjacent release document:

- **Grant**: permission to use name, title, company, and testimonial text.
- **Channels**: specified list (website, proposals, presentations, social media, marketing materials).
- **Duration**: perpetual unless revoked in writing.
- **Modifications**: permission to edit for length/grammar with approval of final version.
- **Photo/logo**: optional permission to use headshot or company logo.
- **Revocation clause**: contact method to withdraw permission at any time.

Provided in both languages. Not a legal contract (disclaimer included); user should consult legal counsel for binding agreements.

### Privacy Considerations

- Always get explicit written permission before publishing.
- Offer anonymization options: full attribution, first name + company only, role + industry only, fully anonymous.
- Track permission status per testimonial in the testimonial bank.
- GDPR/Habeas Data note: testimonials containing personal data fall under data protection regulations.

## Testimonial Formatting

### Standard Format

Every testimonial is structured as:

```
"[Quote text — 1-3 sentences, specific and result-oriented.]"

— [Full Name], [Role/Title], [Company Name]
  Context: [Project type or engagement description]
  Date: [Month Year of engagement]
  Permission: [APPROVED / PENDING / ANONYMOUS]
```

### Quality Tiers

Testimonials are rated by strength for prioritized usage:

| Tier | Criteria | Use For |
|------|----------|---------|
| **S-Tier** | Specific metric + named outcome + full attribution | Homepage hero, proposal cover |
| **A-Tier** | Clear outcome + full attribution, no hard metric | Service pages, deck slides |
| **B-Tier** | Positive sentiment + partial attribution | Supporting social proof sections |
| **C-Tier** | Generic praise or anonymous | Internal confidence only, not for publication |

### Formatting Rules

- **Maximum length**: 280 characters for web display, 500 for proposals.
- **Emphasis**: bold the single most impactful phrase within the quote.
- **Specificity edit**: if original is vague ("they were great"), follow up for specifics before publishing.
- **Tense**: present tense preferred ("JM Labs delivers...") over past tense.
- **No fabrication**: never invent, embellish, or combine quotes from different people.

## Display Patterns

### Web Testimonial Cards

Branded HTML cards for website embedding:

- **Layout**: horizontal scroll carousel or 3-column grid.
- **Card anatomy**: large quotation mark icon, quote text, horizontal rule, avatar placeholder (initials), name, role, company.
- **Brand styling**: JM Labs dark theme (`#0a0a0a` bg, `#e94560` quote marks, `#eaeaea` text).
- **Responsive**: single column on mobile, 2 on tablet, 3 on desktop.
- **Animation**: CSS-only fade-in on scroll (no JavaScript).

### Pitch Deck Format

- One testimonial per slide, large quote text (24pt+), attribution below, dark JM Labs background.
- Suggested placement: after case study slide or before pricing slide.

### Proposal Sidebar Format

- Shortened quote (140 chars max), name and company, contextually matched to the adjacent proposal section.

## Testimonial Bank Structure

The master bank is tracked via `index.csv` with fields: id, client_name, company, tier, permission_status, channels_approved, language, date_collected, last_used_date, usage_count. Individual testimonials stored as `quotes/{client-slug}.md` with full context and permission metadata.

## Trade-off Matrix

| Decision | Option A | Option B | Default |
|----------|----------|----------|---------|
| Collection method | Structured form | Open-ended interview | Structured form (higher completion) |
| Quote editing | Verbatim only | Light editing allowed | Light editing with approval |
| Attribution level | Full name + company | Anonymous by default | Full attribution (higher trust signal) |
| Display format | HTML cards | Markdown + guidelines | HTML cards (ready to use) |
| Testimonial bank | CSV flat file | JSON structured | CSV (universal, editable) |
| Follow-up cadence | One-time ask | Quarterly refresh | One-time with annual refresh reminder |

## Assumptions & Limits

- **Assumption**: user has existing client relationships to draw testimonials from. [INFERRED]
- **Assumption**: testimonials are for professional B2B services context. [INFERRED]
- **Assumption**: user will handle actual outreach; this skill produces the assets and framework. [EXPLICIT]
- **Limit**: no automated email sending or CRM integration.
- **Limit**: no sentiment analysis or NLP processing of responses.
- **Limit**: release template is a guideline, not legal advice; consult counsel for binding agreements.
- **Limit**: no image/headshot generation; avatar placeholders use initials.

## Edge Cases

1. **No testimonials yet**: user has zero collected testimonials. Generate the complete collection toolkit (questions, templates, release form, empty bank structure) as a cold-start kit.
2. **Negative or mixed feedback**: client provides lukewarm testimonial ("it was okay"). Do not publish; instead, generate follow-up questions to understand concerns and potentially improve the relationship before re-asking.
3. **Client requests removal**: previously approved testimonial needs withdrawal. Provide removal checklist (website, cached proposals, deck versions, social posts) and update bank status to REVOKED.
4. **Non-English testimonial**: client provides testimonial in Spanish or Portuguese. Store original language version, provide professional translation for EN usage, mark both versions in bank.
5. **Competitor mention in testimonial**: client says "better than Competitor X". Flag for legal review; comparative advertising has regulatory implications in many jurisdictions.

## Good vs Bad Example

### Good

```
Input: "I need testimonials for my proposal to BancoNacional.
        I worked with TechCorp (Maria Lopez, CTO) on their platform migration
        and with DataFlow (Carlos Ruiz, VP Eng) on their API architecture."

Output:
1. Personalized outreach email for Maria (referencing platform migration).
2. Personalized outreach email for Carlos (referencing API architecture).
3. Question set: Level 1 for email, Level 2 as follow-up.
4. Release template (ES/EN) ready for both contacts.
5. Empty testimonial bank initialized with both contacts as PENDING.
6. Guidance: "For the BancoNacional proposal, an infrastructure testimonial
   from Maria would be most relevant. Place in the Technical Approach section."
```

### Bad

```
Output that:
- Generates fake testimonial quotes attributed to real people
- Sends emails automatically without user review
- Provides a single generic "Dear Client" outreach template
- Skips the permission/release step entirely
- Formats testimonials as a plain text list with no structure
- Ignores the proposal context and target audience
```

## Validation Gate

Before delivering the testimonial assets, verify:

- [ ] No fabricated quotes: every testimonial is from real input or marked as template/placeholder.
- [ ] Permission template included with revocation clause and channel specification.
- [ ] Outreach templates are bilingual (ES/EN) and under word count limits.
- [ ] Each testimonial has complete attribution (name, role, company) or explicit anonymization.
- [ ] Quality tier assigned to each testimonial (S/A/B/C rating).
- [ ] Display patterns use JM Labs brand colors (`#0a0a0a`, `#e94560`, `#eaeaea`).
- [ ] HTML testimonial cards are self-contained (no external dependencies).
- [ ] Testimonial bank structure defined with CSV index schema.
- [ ] Context-matching guidance provided (which testimonial fits which use case).
- [ ] Privacy disclaimer included regarding data protection regulations.
- [ ] No competitor names in testimonials without legal review flag.
- [ ] Print stylesheet included for proposal insertion.

## Reference Files

| File | Purpose |
|------|---------|
| `references/question-bank.md` | Full question set with coaching notes and expected yield |
| `references/release-templates.md` | Permission/release document templates (ES/EN) |
| `references/brand-tokens.md` | JM Labs color palette, typography for testimonial cards |
| `references/display-patterns.md` | HTML/CSS patterns for web, deck, and proposal formats |
