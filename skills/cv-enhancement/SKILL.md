---
name: cv-enhancement
description: >
  Triggers on "improve my CV", "rewrite resume", "enhance CV", "make my CV better",
  "CV for tech role", "mejorar mi hoja de vida", "reescribir CV", "CV para entrevista".
  Produces impact-rewritten CV using PAR framework. Output: markdown + optional branded HTML.
argument-hint: "paste your CV text or describe target role"
model: opus
context: fork
allowed-tools: Read, Write, Edit, Glob, Grep
version: 1.0.0
---

# CV Enhancement — From Duty Descriptions to Impact Stories

> TL;DR: Audit a CV for structural and language weaknesses, rewrite every bullet using the
> PAR framework (Problem-Action-Result), optimize for ATS systems, target to a specific role,
> and deliver a polished markdown CV plus an optional JM Labs dark-branded HTML version.

**Principio Rector:** Hiring managers read CVs for evidence of impact, not lists of
responsibilities. Every bullet must answer: "So what?" If a bullet could belong to anyone
in that role at that company, it has not been rewritten yet.

---

## When to Activate

**Activate when:**
- User says "improve my CV", "rewrite resume", "enhance CV", "make my CV better"
- User says "mejorar mi hoja de vida", "reescribir CV", "CV para entrevista", "ayuda con mi CV"
- User says "CV for tech role", "CV for [specific role/industry]", "help with resume"
- User pastes or shares a CV and asks for feedback, improvement, or transformation [EXPLICIT]
- User is applying to a specific role and wants a targeted, optimized version [INFERRED]
- User mentions ATS, applicant tracking, or keyword optimization in context of their CV [EXPLICIT]

**Do NOT activate when:**
- User asks for cover letter help (different skill — cover letter writing)
- User needs LinkedIn profile optimization (different format, character limits, and strategy)
- User needs a personal portfolio or brand page (use landing-pages or portfolio-sites skill)
- User wants a full career coaching session without a CV to work from (no artifact to transform)
- User provides no CV and no role context — ask for at least one before proceeding

---

## S1: CV Audit

Before rewriting, diagnose what is weak. Apply a structured rubric to the CV as provided.
Share the audit findings with the user before beginning rewrites — confirm scope. [EXPLICIT]

**Structure Audit — section presence and quality:**

| Section | Required | Quality Check |
|---|---|---|
| Contact info | Yes | Email, LinkedIn, city/country; phone optional; no photo in most markets |
| Professional summary | Recommended | 3–4 lines, role-specific, at least one quantified claim |
| Work experience | Yes | Reverse chronological, impact bullets, dates with months |
| Education | Yes | Degree, institution, graduation year; omit GPA unless >3.7 or recent grad |
| Skills | Yes | Categorized (technical, languages, tools), relevant to target role |
| Projects / portfolio | Role-dependent | Mandatory for tech, design, and product roles |
| Certifications | Optional | Include if relevant and issued within last 5 years |
| Publications / talks | Optional | Include for thought leadership, academic, or senior roles |

**Language Quality Audit — patterns to flag and eliminate:** [EXPLICIT]

*Red flags — language to rewrite:*
- Responsibility language: "Responsible for...", "In charge of...", "Duties included..."
- Vague adjectives: "excellent communication skills", "strong team player", "passionate about..."
- Passive voice: "Was involved in...", "Participated in...", "Helped to..."
- Buzzword overload: "synergy", "leverage", "paradigm shift", "disruptive", "thought leader"
- First-person pronouns: "I managed...", "My team..." — drop pronouns entirely in bullet points
- Time-filling phrases: "Worked closely with...", "Was part of the team that..."

*Green flags — language to preserve or generate:*
- Strong action verbs opening every bullet (Led, Built, Reduced, Launched, Negotiated)
- Quantified outcomes: percentages, dollar amounts, time saved, headcount managed, ARR
- Specificity: tool names, stack names, geography, customer segments, deal sizes
- Scope indicators: team size, budget owned, geography covered, revenue line managed

**ATS Readiness Audit:** [EXPLICIT]
- [ ] Standard section headers used (not creative names like "My Story" or "What I've Done")
- [ ] No tables, columns, text boxes, or embedded graphics in the body
- [ ] No content in headers or footers (ATS parsers often skip these areas)
- [ ] File format guidance: clean PDF or .docx — not InDesign/Canva-designed PDFs
- [ ] Standard fonts used (Arial, Calibri, Garamond — no display or decorative fonts)
- [ ] Target job title present in summary and most recent role title
- [ ] Dates include months, not just years (avoids gap misinterpretation by ATS)

**Audit Output Format (share before rewriting):**
```
CV AUDIT SUMMARY
─────────────────────────────────────────────
Sections present:    [list with quality score H/M/L]
Sections missing:    [list with recommendation]
Language red flags:  [count] found — [2-3 example bullets]
ATS issues:          [list of format problems]
Metrics present:     [X out of Y bullets have quantified outcomes]
Overall readiness:   [score /10]
Recommended scope:   [Full rewrite / Targeted edits / Light polish]
─────────────────────────────────────────────
```

---

## S2: PAR Framework

Apply the PAR (Problem-Action-Result) framework to every work experience bullet. [EXPLICIT]
This is the core transformation. Do not skip bullets — every line must pass the PAR test.

**PAR Structure:**
```
P — Problem / Context:  What was the situation, challenge, or goal?
A — Action:             What did YOU specifically do? (your contribution, not the team's)
R — Result:             What measurably improved? (quantify whenever possible)
```

**Compression rule:** Most bullets collapse PAR into one sentence.
Full P+A+R structure is used for the most impactful or complex achievements.

**PAR Transformation Examples:**

| Before (Duty language) | After (PAR-Impact) |
|---|---|
| "Managed social media accounts" | "Grew LinkedIn following from 2K to 18K in 8 months by launching a weekly expert series, driving 340% increase in inbound leads" |
| "Worked on backend API development" | "Engineered REST API handling 50K req/day for fintech product, reducing p95 latency from 800ms to 120ms via Redis caching layer" |
| "Led sales team" | "Led 8-person enterprise sales team to 127% of annual quota ($4.2M ARR), closing 3 Fortune 500 accounts in Q3 2023" |
| "Responsible for data analysis" | "Built automated reporting pipeline (Python + BigQuery) reducing weekly analysis time from 16h to 2h, enabling weekly board reviews" |
| "Helped improve customer satisfaction" | "Redesigned onboarding flow for 12K users, lifting 30-day retention from 41% to 67% and reducing support tickets by 38%" |

**Metrics Injection Protocol** — when the CV lacks numbers: [INFERRED]

If the user's CV has no metrics, do one of two things:
1. Use scope proxies that do not require fabrication (team size, geography, revenue line, customer count)
2. Ask the user directly with targeted questions before finalizing the bullet

*Scope proxies (no fabrication required):*
- Team size managed → scope indicator ("led a 12-person cross-functional team")
- Budget managed → business impact proxy ("oversaw $1.2M annual marketing budget")
- Project count per year → delivery capacity ("delivered 8 client engagements per year")
- Geography → scale indicator ("across 6 Latin American markets")
- Revenue impacted vs. cost center → P&L relevance

*Targeted questions to prompt user for missing metrics:*
- "What % did [metric] change during your tenure?"
- "How many people did you manage directly vs. indirectly?"
- "What was the budget or ARR you were responsible for?"
- "How much time or cost did the improvement save per month/quarter?"
- "What was the before-and-after state you're most proud of in this role?"

> [EXPLICIT] Metrics must be truthful. Never fabricate numbers. If the user cannot
> confirm a metric, use a scope proxy or leave the claim qualitative but specific.

**Action Verb Bank by Category:**

| Category | Verbs |
|---|---|
| Leadership | Led, Directed, Coached, Mentored, Built, Scaled, Reorganized, Championed, Spearheaded |
| Technical | Engineered, Architected, Developed, Automated, Migrated, Optimized, Deployed, Integrated |
| Analysis | Analyzed, Evaluated, Modeled, Forecasted, Benchmarked, Diagnosed, Quantified, Identified |
| Commercial | Closed, Negotiated, Grew, Expanded, Converted, Retained, Upsold, Acquired, Prospected |
| Operations | Streamlined, Reduced, Eliminated, Standardized, Implemented, Launched, Delivered, Managed |
| Communication | Presented, Facilitated, Published, Authored, Trained, Influenced, Partnered, Translated |

---

## S3: Section Rewrites

Rewrite each CV section with role-specific and level-appropriate language. [EXPLICIT]

**Professional Summary / Profile**
The summary is the first-read section. Must be: role-specific (not generic), 3–4 lines,
and contain at least one quantified claim or scope signal.

*Bad:* "Experienced professional with strong communication skills and a passion for results."
*Good:* "Senior product manager with 8 years building B2B SaaS products. Led 0-to-1 launch
of [Product] reaching $2.4M ARR in 14 months. Specializes in data-driven roadmapping,
cross-functional alignment, and enterprise go-to-market. Based in Bogotá, open to remote."

**Work Experience Bullets**
Apply PAR to every bullet. Aim for 3–5 bullets per role. More recent roles get more bullets.
Order bullets within a role: most impactful first, not chronological. No bullet should read
like a job description. Every bullet should read like evidence of value delivered.

**Skills Section**
Structure as named categories, not a flat undifferentiated list:
```
Technical:   Python, SQL, dbt, Snowflake, Tableau, Looker
Frameworks:  Scrum, SAFe, OKRs, Lean Six Sigma
Languages:   Spanish (native), English (C1), Portuguese (B2)
Tools:       JIRA, Confluence, Salesforce, Figma
```
Remove entry-level-expected skills for the target role (e.g., "Microsoft Word" for a senior PM).
Keep only differentiating or explicitly required skills.

**Education**
- Degree + Institution + Graduation Year (month optional)
- Omit GPA unless it is >3.7 and the user graduated within the last 5 years
- Include relevant honors or thesis topic only if directly relevant to the target role
- For senior professionals (10y+): education moves to the bottom — experience leads

**Certifications**
- Include with issuing body and expiry or renewal date if applicable
- Prioritize certifications that appear in the target job posting
- Remove outdated or irrelevant certifications (>7 years old, unrelated field)

---

## S4: ATS Optimization

Ensure the CV passes automated screening before it reaches a human reviewer. [EXPLICIT]

**Keyword Strategy (4-step process):**
1. Take the target job description (user provides or names the role + company)
2. Extract 15–20 keywords: job titles, skills, tools, certifications, methodologies [EXPLICIT]
3. Map each keyword to the CV section where it is (or should be) mentioned [INFERRED]
4. Insert missing high-priority keywords naturally — no keyword stuffing [EXPLICIT]

**Keyword Categories by ATS Weight:**

| Category | ATS Weight | Examples |
|---|---|---|
| Job title match | Very High | "Product Manager", "Senior Data Engineer" |
| Hard technical skills | High | "Python", "Salesforce", "AWS", "dbt" |
| Certifications | High | "PMP", "AWS Solutions Architect", "CISSP" |
| Industry terms | Medium | "SaaS", "fintech", "HIPAA", "GDPR", "ISO 27001" |
| Methodologies | Medium | "Scrum", "Agile", "Kanban", "Six Sigma" |
| Soft skills | Low | "leadership", "communication" — use sparingly |

**Formatting Rules for ATS Compliance:**

| Rule | Rationale |
|---|---|
| Use `.docx` or clean PDF | Designer PDFs (Canva, InDesign) often fail ATS parsing |
| No columns or tables for experience | Column parsers split dates from content |
| Spell out acronyms first use | "Machine Learning (ML)" before using "ML" alone |
| Include months AND years | "Jan 2022 – Mar 2024" not "2022 – 2024" |
| Standard date format | Prevents duration calculation errors in ATS |
| No images, icons, or logos in body | ATS ignores or errors on visual elements |
| Standard section headers | "Work Experience" not "Where I've Worked" |
| Left-aligned text | Centered or right-aligned body text can confuse parsers |

**Keyword Density Check (after rewriting):**
- Target job title appears in summary AND most recent role section
- Top 5 technical skills appear at least 2× across the document
- No single keyword used >5× — excessive repetition triggers ATS spam filters [INFERRED]
- Industry-specific compliance terms included if the role requires them

---

## S5: Role Targeting

Customize the CV for a specific job posting or industry vertical. [EXPLICIT]

**Single-Role Targeting (when user provides a specific posting):**
1. Extract must-have vs. nice-to-have requirements from the job description [EXPLICIT]
2. Reorder bullets within each role to front-load most relevant experience [INFERRED]
3. Adjust professional summary to mirror the role's specific language [EXPLICIT]
4. Rename or reframe job titles if truthful and more ATS-friendly [EXPLICIT]
5. Surface or expand relevant projects that match the posting's requirements [INFERRED]
6. Add a "Relevant Experience" section if the overall match is partial [INFERRED]

**Industry-Specific Calibrations:**

| Industry | Key Adjustments |
|---|---|
| Tech / SaaS | Stack-first ordering, quantified engineering impact, GitHub or portfolio link |
| Finance | Regulatory knowledge (SOX, Basel, MiFID), deal size, P&L ownership, CFA/CPA |
| Consulting | Client count, engagement scope, industry verticals served, frameworks used |
| Healthcare | Certifications (HIPAA, HITECH), patient outcomes, EHR systems, compliance |
| Startups | Bias-to-action verbs, generalist range, 0-to-1 initiatives, scrappy resourcefulness |
| Enterprise | Scale, governance, stakeholder management, budget size, cross-org impact |
| Sales | Quota attainment %, deal size, sales cycle length, named accounts, CRM proficiency |
| Product | OKRs owned, revenue impact, user growth metrics, cross-functional leadership |

**Career Level Calibrations:**

| Level | Summary Focus | Bullet Depth | Format Bias |
|---|---|---|---|
| Junior (0–3y) | Skills, education, projects | Task + tool + learning outcome | 1 page max |
| Mid (3–7y) | Results + growth trajectory | PAR with metrics | 1–2 pages |
| Senior (7–15y) | Leadership + strategy | Business impact + team and org scope | 2 pages |
| Executive (15y+) | Vision + P&L + org transformation | Revenue, company-wide change | 2 pages max |

**Career Change Targeting** (switching tracks entirely):
- Switch to skills-first format: Skills section moves above Experience
- Emphasize transferable skills with PAR bullets showing adaptability
- Reframe past experience in the language of the target industry
- Add a "Relevant Projects" section to surface new-track work (side projects, courses, volunteer)
- Summary must explicitly acknowledge the transition with a confident forward-looking narrative

---

## S6: Output Formats

Two output formats. Produce markdown by default; produce HTML when user requests it. [EXPLICIT]

**Format A: Markdown CV** — clean, portable, ATS-safe for digital job submissions:

```markdown
# [Full Name]
[City, Country] · [email@domain.com] · [linkedin.com/in/handle]

## Professional Summary
[3–4 lines. Role-specific. At least one quantified claim. No first-person pronouns.]

## Experience

### [Job Title] — [Company Name], [City / Remote]
*[Mon YYYY] – [Mon YYYY]*
- [PAR bullet — strongest impact first]
- [PAR bullet — second most relevant]
- [PAR bullet — third]

### [Previous Job Title] — [Company Name], [City]
*[Mon YYYY] – [Mon YYYY]*
- [PAR bullet]
- [PAR bullet]

## Skills
**Technical:** [comma-separated list]
**Frameworks:** [comma-separated list]
**Languages:** [Language (Level), Language (Level)]
**Tools:** [comma-separated list]

## Education
**[Degree, Field]** — [Institution Name], [Year]

## Certifications
- [Certification Name] — [Issuing Body] ([Year])
```

**Format B: Branded HTML CV** — JM Labs dark design system, for portfolio sharing.
Self-contained single file. Not for ATS submission. Includes `@media print` CSS. [EXPLICIT]

Load the full HTML template from `references/html-cv-template.md` when producing Format B.

**JM Labs Brand Tokens (required for HTML output):**
```css
:root {
  --bg:    #0d0d0d;
  --card:  #1a1a2e;
  --navy:  #122562;
  --gold:  #FFD700;
  --blue:  #137DC5;
  --text:  #e0e0e0;
  --muted: #9e9e9e;
  --font-h: 'Poppins', sans-serif;
  --font-b: 'Inter', sans-serif;
}
```

**HTML CV Structure (sections in order):**
1. `<header>` — Name (gold), target role title (blue), contact bar (muted text + linked email/LinkedIn)
2. Summary block — dark card, gold left border, 3–4 lines, no pronouns
3. Experience section — one `.role` card per position (gold title, muted dates, PAR bullet list with gold triangles)
4. Skills grid — 2–4 category cards (Poppins label in gold, Inter body in white)
5. Education — single row cards (degree in gold, institution + year muted)
6. Certifications — optional, same card pattern as education
7. `<footer>` — "Generated with JM Labs CV Enhancement · [DATE]" in muted text

**Bilingual support:** Add `[data-l="es"]` / `[data-l="en"]` on section titles and labels
for clients who need to switch language of the CV display without re-generating. [EXPLICIT]

**Print CSS requirement:** Include `@media print` block that switches to white background,
`#122562` for headings, `#f8f8f8` for cards. Page-break-inside: avoid on `.role` blocks. [EXPLICIT]

> [EXPLICIT] HTML output is for portfolio sharing and direct recruiter review.
> For ATS submission, always provide the markdown version as clean PDF or .docx.
> HTML-only CVs will not parse correctly in most ATS systems.

---

## Trade-off Matrix

| Decision | Option A | Option B | Recommendation |
|---|---|---|---|
| Impact language vs. factual accuracy | Maximize impact phrasing | Stay strictly literal | Impact is fine; fabricating numbers is not. Scope proxies resolve the gap. |
| ATS optimization vs. human readability | Dense keywords, standard format | Natural writing, design-forward | ATS-first for applications; human-first for networking/sharing versions |
| Breadth vs. depth per role | Many bullets, wide coverage | 3–5 bullets, highest impact only | Fewer, stronger bullets always outperform long lists of mediocre ones |
| Generalist vs. targeted summary | Generic summary for all roles | Role-specific summary per application | Role-specific always wins for conversion rate |
| One-page vs. two-page | Strict one page | Two pages for senior | Junior: one page max. Mid and above: two pages fine. Executive: two pages max. |
| Markdown vs. HTML output | Clean markdown (ATS-safe) | Branded HTML (visual, shareable) | Markdown for job applications; HTML for portfolio, LinkedIn share, recruiter outreach |

---

## Assumptions & Limits

- [EXPLICIT] User must provide the CV content (file path, pasted text, or dictated experience)
- [EXPLICIT] Metrics must be truthful — the skill prompts for real numbers, never fabricates them
- [EXPLICIT] ATS optimization is calibrated to major systems: Workday, Greenhouse, Lever, Taleo
- [EXPLICIT] HTML output is for sharing and portfolio use — not ATS-safe; always provide markdown too
- [EXPLICIT] Career history reframing must be factually accurate — role inflation is not permitted
- [INFERRED] Keyword strategy requires user to name a target role or provide a job description;
  without this, optimization is generalized to the user's most recent role level and function
- [OPEN] ATS parsing logic varies by system and version; optimization targets known patterns,
  not guaranteed results across every platform

---

## Edge Cases

| Scenario | Handling |
|---|---|
| CV in Spanish, target role in English | Translate + adapt: idioms, title conventions, and metric framing differ by market. Produce English version; offer bilingual HTML if requested. |
| Career gap of >12 months | Address directly in the summary with positive framing: freelance, caregiving, further education, sabbatical. Do not hide or obscure the gap. |
| Career change (different track entirely) | Switch to skills-first format. Add "Relevant Projects" section. Reframe past experience in the target industry's language. Summary leads with the pivot narrative. |
| Academic CV (publications-heavy) | Switch to academic format conventions. Do not strip the publications section. Add teaching experience, grants, and committee roles if present. |
| New graduate / <1 year experience | Amplify projects, coursework, internships, hackathons, volunteer work. Education section leads over experience. One page strictly. |
| Long tenure in one role (8y+ same company) | Break the role into sub-roles or initiative clusters if scope changed significantly. Prevents appearance of stagnation. |
| User refuses to provide any metrics | Use scope proxies throughout. Note in output that metrics are scope-based, not outcome-based. |

---

## Good vs. Bad Example

**BAD — Duty language, no impact:**
> "Responsible for managing the development team and ensuring project delivery."

**GOOD — PAR-transformed, specific, quantified:**
> "Led 6-person cross-functional engineering team delivering 3 major product releases in 2023,
> reducing deployment cycle from 3 weeks to 5 days through CI/CD pipeline implementation
> (GitHub Actions + Docker)."

**Analysis of the transformation:**
- "Responsible for managing" → "Led [X-person]" — action verb + concrete scope
- "ensuring project delivery" → "delivering 3 major product releases in 2023" — specific and countable
- Before/after metric added: "3 weeks to 5 days" — quantifies the impact
- Tools named: "GitHub Actions + Docker" — ATS keywords + technical credibility
- No fabrication: team size and tool names are facts the user can confirm independently

---

## Validation Gate

Before delivering any CV output, verify all of the following:

- [ ] CV structure audit completed — all required sections present and quality-assessed
- [ ] Red-flag language patterns identified and eliminated across all sections
- [ ] Every work experience bullet opens with a strong action verb (no "Responsible for")
- [ ] At least 70% of bullets contain a quantified metric or measurable scope indicator
- [ ] ATS formatting rules applied: no columns, standard headers, no images in body
- [ ] Top 10 keywords from target role incorporated naturally (no stuffing)
- [ ] Professional summary is role-specific, 3–4 lines, contains at least one quantified claim
- [ ] Markdown CV output is clean, portable, and free of formatting artifacts
- [ ] HTML output uses JM Labs brand tokens (navy `#122562`, gold `#FFD700`, blue `#137DC5`, dark bg)
- [ ] HTML output includes `@media print` CSS and `[data-l]` bilingual attributes on section labels

---

## Reference Files

| File | Purpose |
|---|---|
| `knowledge/body-of-knowledge.md` | CV writing methodology and PAR framework research |
| `references/html-cv-template.md` | Full JM Labs branded HTML CV template |
| `evals/` | Before/after CV examples with scoring rubric |

---

## Related Skills

- `landing-pages` — Personal brand page to complement the CV
- `b2b-outreach` — Craft outreach messages using CV highlights as professional credentials
- `executive-pitch` — Translate career story into a compelling 5-minute verbal pitch
- `ux-writing` — Microcopy principles applicable to tight, scannable bullet writing
