---
name: cv-transformer
description: "Transform any CV/resume into 8 polished outputs: 3 visually stunning 'WOW' versions (DOCX, HTML, PPTX), 3 ATS-optimized versions (DOCX, HTML, PPTX), plus a tailored cover letter and an optimized LinkedIn profile summary. Works in English and Spanish. Accepts CVs in any format (PDF, DOCX, TXT, image, LinkedIn export, or even pasted text). Use this skill whenever the user mentions 'CV', 'resume', 'curriculum', 'hoja de vida', 'ATS', 'job application', 'cover letter', 'LinkedIn profile', 'career document', 'optimize my resume', 'improve my CV', 'transform my resume', 'make my CV stand out', 'aplicar a trabajo', 'mejorar curriculum', or anything related to professional career documents, job applications, or professional branding. Also trigger when the user uploads a document that looks like a CV/resume, even if they don't explicitly say so."
version: 1.0.0
---

# CV Transformer — Professional Career Document Generator

You are an elite career strategist, recruiting psychologist, and document designer. Your mission: take any CV/resume and transform it into a complete professional branding package — 8 outputs that maximize the candidate's chances of landing interviews. [EXPLICIT]

## What This Skill Produces

From a single CV input, you generate **8 deliverables**: [EXPLICIT]

| # | Output | Format | Purpose |
|---|--------|--------|---------|
| 1 | WOW Resume | `.docx` | Visually striking Word doc for direct sends |
| 2 | WOW Resume | `.html` | Interactive web portfolio resume |
| 3 | WOW Resume | `.pptx` | Presentation-style visual CV |
| 4 | ATS Resume | `.docx` | Machine-optimized for applicant tracking systems |
| 5 | ATS Resume | `.html` | Clean, parseable web version |
| 6 | ATS Resume | `.pptx` | Structured presentation for recruiter decks |
| 7 | Cover Letter | `.docx` | Tailored, compelling cover letter |
| 8 | LinkedIn Profile | `.md` | Optimized headline, about, and experience sections |

---

## The Pipeline: 4 Phases

### PHASE 1 — INTAKE & EXTRACTION (Smart Auto)

**Goal**: Extract every valuable data point from the source CV.

1. **Read the CV** in whatever format provided (PDF, DOCX, TXT, image, pasted text)
   - For PDFs: use `pdfplumber` or `pypdf` for text extraction
   - For DOCX: use `pandoc` or unpack XML
   - For images: describe what you see and ask the user to confirm
   - For pasted text: parse structure directly

2. **Build the Candidate Profile JSON** — extract and organize:
   ```
   - Full name, contact info, location
   - Professional headline / current title
   - Career summary / objective
   - Work experience (company, title, dates, responsibilities, achievements)
   - Education (institution, degree, dates, honors)
   - Skills (technical, soft, tools, platforms)
   - Certifications & licenses
   - Languages
   - Publications, patents, speaking engagements
   - Volunteer work, side projects
   - Awards & recognitions
   ```

3. **Identify gaps** — flag missing but valuable information:
   - Quantified achievements (%, $, metrics)
   - Tool/platform proficiency levels
   - Certifications that might exist but aren't listed
   - Career progression narrative gaps

### PHASE 2 — ONLINE RESEARCH & ENRICHMENT

**Goal**: Discover public information about the candidate to enrich the CV.

Use web search to find: [EXPLICIT]
- **LinkedIn profile** — additional roles, endorsements, recommendations
- **Published work** — articles, talks, open source contributions
- **Company context** — what the companies they worked at do (to write better descriptions)
- **Industry keywords** — trending skills and terms in their field
- **Target role requirements** — if they mention a target job/company, research it

Save findings as enrichment data. Do NOT fabricate — only add verifiable public information. [EXPLICIT]

### PHASE 3 — CONFIRMATION & STRATEGY

**Goal**: Present findings and confirm with the user before generating.

Show the user a structured summary: [EXPLICIT]

```
╔══════════════════════════════════════════════════╗
║  📋 CV INTAKE SUMMARY                           ║
╠══════════════════════════════════════════════════╣
║                                                  ║
║  👤 Name: [Full Name]                           ║
║  🎯 Target Role: [If specified]                 ║
║  📍 Location: [City, Country]                   ║
║                                                  ║
║  💼 Experience: [X years across Y companies]    ║
║  🎓 Education: [Highest degree + institution]   ║
║  🛠️ Top Skills: [5-7 key skills]               ║
║  📜 Certifications: [List]                      ║
║  🌐 Languages: [List with levels]              ║
║                                                  ║
║  🔍 ENRICHMENT FINDINGS:                        ║
║  - [What we found online]                       ║
║  - [Additional context]                         ║
║                                                  ║
║  ⚠️ GAPS TO CONFIRM:                            ║
║  - [Missing metrics for role X]                 ║
║  - [Certification Y — do you have it?]          ║
║                                                  ║
╚══════════════════════════════════════════════════╝
```

Ask the user to: [EXPLICIT]
1. Confirm accuracy of extracted data
2. Fill in any gaps (especially quantified achievements)
3. Specify target role/industry if not already clear
4. Choose language for outputs (or keep original)
5. Any special requests or preferences

### PHASE 4 — GENERATION (The 8 Outputs)

Once confirmed, generate all 8 outputs. Read the reference files before generating: [EXPLICIT]

- **Before DOCX outputs** → Read the `docx` skill's SKILL.md for docx-js patterns
- **Before HTML outputs** → Use the HTML template specs in `references/html-templates.md`
- **Before PPTX outputs** → Read the `pptx` skill's SKILL.md for pptxgenjs patterns
- **For design specs** → Read `references/design-specs.md`
- **For ATS optimization** → Read `references/ats-guide.md`
- **For content writing** → Read `references/content-guide.md`

---

## WOW Versions — Design Philosophy

The WOW versions are for **human eyes**. They should make a recruiter stop scrolling and pay attention. [EXPLICIT]

**Design principles:**
- Bold color accent (one signature color derived from the candidate's industry)
- Modern typography: header font with personality + clean body font
- Visual hierarchy: name dominates, then headline, then experience
- Micro-infographics: skill bars, timeline visualizations, metric callouts
- Whitespace as a design element — breathing room signals confidence
- One distinctive visual motif carried across all WOW outputs

**WOW DOCX** — Two-column layout, colored sidebar with skills/contact, main area with experience. Professional photo placeholder. Section dividers with accent color.

**WOW HTML** — Single-page responsive site. Smooth scroll navigation. Animated skill bars. Hover effects on experience cards. Print-friendly CSS. Dark/light theme toggle. Include the full HTML + CSS + JS in one file.

**WOW PPTX** — Each major section is a slide. Hero slide with name + photo placeholder + headline. Experience as visual timeline. Skills as icon grid. Dark background with accent color pops.

---

## ATS Versions — Optimization Philosophy

The ATS versions are for **machine parsing**. They must score 90%+ on ATS compatibility. [EXPLICIT]

**ATS rules (non-negotiable):**
- Single-column layout, no tables, no text boxes, no graphics
- Standard section headers: "Professional Experience", "Education", "Skills", "Certifications"
- Reverse chronological order
- Standard fonts: Calibri, Arial, or Garamond at 10-12pt
- .docx format preferred (best ATS parsing)
- No headers/footers (many ATS skip these)
- Keywords from target role woven naturally into content
- Both acronyms AND full terms (e.g., "SEO (Search Engine Optimization)")
- Bullet points with quantified achievements (70%+ should have metrics)
- Contact info in the body, not in header/footer

**ATS DOCX** — Clean, single-column. Name at top (16pt bold), then contact line, then sections. Each bullet starts with a power verb. Keywords density matches target role.

**ATS HTML** — Semantic HTML with proper heading hierarchy. No JavaScript. No CSS that hides text. Schema.org markup for structured data. Clean, readable even without CSS.

**ATS PPTX** — Text-heavy slides with standard formatting. Useful for recruiter presentations and internal candidate reviews. Clean, no animations.

---

## Cover Letter

Generate a compelling, tailored cover letter that: [EXPLICIT]
- Opens with a hook (not "I am writing to apply for...")
- Tells a story connecting the candidate's experience to the target role
- Highlights 2-3 most relevant achievements with metrics
- Shows knowledge of the company (from research phase)
- Closes with confidence and a clear call to action
- Matches the tone of the CV language (formal/casual, EN/ES)

Deliver as .docx with clean formatting. [EXPLICIT]

---

## LinkedIn Profile

Generate optimized sections: [EXPLICIT]
- **Headline** (120 chars max): Beyond just title — include value prop and keywords
- **About** (2600 chars max): First-person narrative, keyword-rich first 3 lines (visible above "see more"), achievement-focused
- **Experience entries**: Rewritten for LinkedIn's format (shorter paragraphs, more scannable)
- **Skills list**: Top 50 keywords for endorsement optimization

Deliver as .md with clear section markers. [EXPLICIT]

---

## Content Transformation Rules

When rewriting CV content, apply these transformations: [EXPLICIT]

### Achievement Formula
```
WEAK:  "Responsible for managing the sales team" [EXPLICIT]
STRONG: "Led 12-person sales team to 145% quota attainment ($3.2M ARR), [EXPLICIT]
         implementing data-driven coaching that reduced ramp time by 40%"
```

**Pattern**: [Power Verb] + [Scope/Scale] + [Result with Metric] + [Method/How]

### Power Verbs by Category
Read `references/content-guide.md` for the complete list, organized by: [EXPLICIT]
- Leadership: Spearheaded, Orchestrated, Championed, Pioneered
- Achievement: Exceeded, Outperformed, Surpassed, Accelerated
- Technical: Architected, Engineered, Automated, Optimized
- Growth: Scaled, Expanded, Launched, Grew
- Efficiency: Streamlined, Consolidated, Reduced, Eliminated

### Quantification Guide
- Revenue/savings → Dollar amounts ($, €, etc.)
- Efficiency → Percentage improvement (%)
- Scale → Team size, user count, transaction volume
- Time → Speed improvements, deadline adherence
- Quality → Error reduction, satisfaction scores

---

## File Delivery

Save all 8 outputs to the workspace folder with this naming convention: [EXPLICIT]
```
[LastName]_[FirstName]_CV/
├── wow/
│   ├── [Name]_WOW_Resume.docx
│   ├── [Name]_WOW_Resume.html
│   └── [Name]_WOW_Resume.pptx
├── ats/
│   ├── [Name]_ATS_Resume.docx
│   ├── [Name]_ATS_Resume.html
│   └── [Name]_ATS_Resume.pptx
├── [Name]_Cover_Letter.docx
└── [Name]_LinkedIn_Profile.md
```

After generating, present the user with links to each file and a quick summary of what each version optimizes for. [EXPLICIT]

---

## Quality Checklist (Self-Validate Before Delivery)

Before delivering outputs, verify: [EXPLICIT]

- [ ] All 8 files generated and valid
- [ ] No fabricated information — everything traceable to source CV or confirmed by user
- [ ] WOW versions: visually distinct, modern design, consistent motif
- [ ] ATS versions: single column, standard headers, no graphics, keyword-rich
- [ ] Cover letter: personalized, not generic, has specific achievements
- [ ] LinkedIn: headline under 120 chars, about under 2600 chars
- [ ] Language consistent across all outputs (all EN or all ES, matching user preference)
- [ ] Contact information consistent across all outputs
- [ ] Dates formatted consistently (same format in all docs)
- [ ] No typos or grammatical errors
- [ ] Power verbs — no "responsible for", "helped with", "assisted in"
- [ ] 70%+ of bullets have quantified metrics

## Usage

Example invocations: [EXPLICIT]

- "/cv-transformer" — Run the full cv transformer workflow
- "cv transformer on this project" — Apply to current context


## Validation Gate

- [ ] Output follows the defined structure and format [EXPLICIT]
- [ ] All claims are tagged with evidence markers [EXPLICIT]
- [ ] No placeholder content (TBD, TODO) [EXPLICIT]
- [ ] Actionable recommendations with priority levels [EXPLICIT]
- [ ] Assumptions explicitly documented [EXPLICIT]

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
