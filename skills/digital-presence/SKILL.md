---
name: digital-presence
description: >
  Triggers on "digital presence audit", "online presence", "presencia digital", "audit my online footprint".
  Conducts online footprint audits covering search results, social profiles, domain authority,
  brand consistency, and reputation signals. Output: branded HTML audit report with scores. [EXPLICIT]
argument-hint: "Brand or person name, primary domain, social profile URLs, and target audience"
model: opus
context: fork
allowed-tools: Read, Write, Edit, Glob, Grep
version: 1.0.0
---

# digital-presence

> **TL;DR** — Produces a comprehensive digital presence audit that scores brand visibility, consistency, reputation, and SEO posture across channels, delivering actionable recommendations in a branded HTML report.

---

## When to Activate

Invoke this skill when any of these conditions are met:

| Signal | Examples |
|--------|----------|
| Presence audit request | "Audit our digital presence", "How do we look online?" |
| Brand consistency check | "Are our social profiles aligned with our brand guidelines?" |
| Reputation assessment | "What shows up when you Google our company name?" |
| Pre-launch review | "Before we launch, check our online footprint" |
| Competitive benchmarking | "How does our online presence compare to competitor X?" |

Do **not** activate for deep SEO technical audits (use `seo-architecture`), social media content calendars (use `content-calendar`), or paid advertising analysis.

---

## 1. Audit Scope Definition

Before conducting the audit, establish boundaries:

- **Subject** — company name, personal brand, or product name being audited.
- **Primary domain** — the canonical website URL.
- **Social channels in scope** — LinkedIn, Twitter/X, Instagram, YouTube, GitHub, TikTok, Facebook, or others relevant to the subject.
- **Geographic focus** — which markets matter (affects search result interpretation).
- **Competitor set** — up to three competitors for relative benchmarking (optional).
- **Target audience** — who should be impressed by the digital presence (investors, customers, talent, partners).

If the user provides only a name and domain, proceed with a standard audit and flag missing channels as findings.

---

## 2. Audit Dimensions & Scoring Framework

The audit evaluates seven dimensions, each scored 1-10:

### 2.1 Search Visibility (Weight: 20%)
- First-page Google results for brand name: owned vs third-party vs negative.
- Knowledge panel presence and accuracy.
- Featured snippets or People Also Ask ownership.
- Brand name search volume trend (directional: growing, stable, declining). [INFERRED]

### 2.2 Social Profile Completeness (Weight: 15%)
- Profile photo, cover image, bio consistency across platforms.
- Contact information accuracy and call-to-action presence.
- Profile URL optimization (vanity URLs vs default strings).
- Verification badges where applicable.

### 2.3 Content Freshness (Weight: 15%)
- Last post date per channel. Flag channels with 90+ days of inactivity.
- Posting frequency and consistency patterns.
- Content type diversity (text, image, video, documents).

### 2.4 Brand Consistency (Weight: 15%)
- Visual identity alignment (logo, colors, typography) across channels.
- Messaging consistency (tagline, value proposition, tone of voice).
- Naming consistency (exact brand name vs abbreviations vs misspellings).

### 2.5 Domain Authority & Technical SEO Snapshot (Weight: 15%)
- Domain age and registration status (WHOIS-based).
- SSL certificate status and configuration.
- Mobile responsiveness signal.
- Page speed category (fast, moderate, slow) based on available signals. [INFERRED]
- Structured data / schema markup presence.

### 2.6 Reputation Signals (Weight: 10%)
- Review platforms (Google Business, Trustpilot, G2, Glassdoor) — average rating and volume.
- Negative press or complaint signals on first two pages of search results.
- Mentions in authoritative publications or directories.

### 2.7 Engagement Quality (Weight: 10%)
- Follower-to-engagement ratio on primary social channels.
- Comment sentiment patterns (positive, neutral, negative). [INFERRED]
- Community responsiveness — does the brand reply to comments and messages?

---

## 3. Report Structure

The output report follows this layout:

1. **Executive Summary** — overall score (weighted average of 7 dimensions), top 3 strengths, top 3 vulnerabilities, priority actions.
2. **Scorecard Table** — all 7 dimensions with individual scores, weights, and weighted contribution.
3. **Dimension Deep Dives** — one section per dimension with findings, evidence, and specific recommendations.
4. **Competitive Comparison** (if competitors provided) — side-by-side scorecard with gap analysis.
5. **Action Plan** — prioritized list of recommended improvements, grouped by effort level (quick wins, medium effort, strategic investments).
6. **Methodology Note** — disclosure of what was assessed, data limitations, and evidence tags.

---

## 4. Output Formatting

- **HTML mode** (default for this skill): self-contained HTML with inline CSS. Color-coded scores (green 8-10, amber 5-7, red 1-4). Radar chart approximation using CSS. Section navigation links.
- **Markdown mode**: available on request, suitable for inclusion in larger documents.
- All scores accompanied by brief justification text.
- Footer: `Generated by digital-presence skill | {subject} | {date}`.

---

## Trade-off Matrix

| Dimension | Priority | Rationale |
|-----------|----------|-----------|
| Actionability | HIGH | Scores without recommendations are useless |
| Evidence quality | HIGH | Every finding must cite observable signals |
| Completeness | MEDIUM | Cover all 7 dimensions but depth varies by data availability |
| Visual polish | MEDIUM-HIGH | HTML output represents the brand analysis standard |
| Speed | LOW | Thoroughness matters more than turnaround |

---

## Assumptions & Limits

1. The skill operates on information the user provides or describes — it does not autonomously crawl websites or query APIs. [EXPLICIT]
2. Domain authority scores are estimated from contextual signals, not live Moz/Ahrefs data. [INFERRED]
3. Sentiment analysis is directional, not statistically rigorous. [INFERRED]
4. Search visibility assessment is based on user-reported results or general knowledge, not real-time SERP scraping. [EXPLICIT]
5. Competitive benchmarking requires the user to supply competitor profile URLs or basic data. [EXPLICIT]
6. The audit is a point-in-time snapshot; ongoing monitoring requires a separate tool or service. [EXPLICIT]

---

## Edge Cases

1. **Brand name is a common word** — adjust search visibility methodology to focus on branded queries with qualifiers (e.g., "Acme software" not just "Acme"). Note disambiguation challenges in the report.
2. **Personal brand vs corporate brand** — adapt the template: personal brands emphasize LinkedIn, personal website, and speaking engagements; corporate brands emphasize Google Business, review platforms, and domain authority.
3. **No social media presence at all** — score social dimensions as 1/10 and frame the entire report as a greenfield digital presence strategy rather than an audit.
4. **Negative reputation crisis** — if the user reports active negative press, elevate the reputation section to the top of the report and add a crisis response recommendations section.

---

## Good vs Bad Example

**Good output** (excerpt):
```
## Scorecard

| Dimension | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Search Visibility | 7/10 | 20% | 1.40 |
| Social Completeness | 4/10 | 15% | 0.60 |
| Content Freshness | 3/10 | 15% | 0.45 |
| Brand Consistency | 6/10 | 15% | 0.90 |
| Domain & SEO | 8/10 | 15% | 1.20 |
| Reputation Signals | 7/10 | 10% | 0.70 |
| Engagement Quality | 5/10 | 10% | 0.50 |
| **Overall** | | | **5.75/10** |

### Top Vulnerability: Content Freshness (3/10)
LinkedIn last posted 127 days ago. Instagram has no posts in 2026.
Twitter/X account exists but has only 3 posts total. [EXPLICIT]

**Recommendation:** Establish a minimum viable posting cadence of
2x/week on LinkedIn and 1x/week on the secondary channel.
```

**Bad output** (excerpt):
```
## Digital Presence
Your online presence is okay. You have some social media accounts
and a website. You could probably post more and update your profiles.
Score: 6/10.
```

The good example provides per-dimension scores with evidence and specific recommendations. The bad example is vague, lacks structure, and provides an unjustified aggregate score.

---

## Validation Gate

Before delivering the audit report, confirm every item:

- [ ] Subject identity (brand/person name and primary domain) is clearly stated
- [ ] All seven audit dimensions are scored individually with justification
- [ ] Weighted overall score is calculated correctly
- [ ] Top strengths and top vulnerabilities are explicitly called out
- [ ] Each dimension section includes at least one specific, actionable recommendation
- [ ] Evidence tags are applied to all claims (EXPLICIT, INFERRED, or OPEN)
- [ ] Competitive comparison included if competitor data was provided
- [ ] Action plan is prioritized by effort level
- [ ] HTML output uses color-coded scores and is self-contained
- [ ] Methodology note discloses data limitations transparently
- [ ] Output file written to disk at confirmed path

---

## Reference Files

| File | Purpose |
|------|---------|
| `references/audit-template.html` | Branded HTML audit report template with scoring layout |
| `references/scoring-rubric.md` | Detailed 1-10 scoring criteria for each audit dimension |
| `references/body-of-knowledge.md` | Digital presence audit methodologies and industry benchmarks |
| `evals/evals.json` | Evaluation scenarios for audit completeness and scoring accuracy |
