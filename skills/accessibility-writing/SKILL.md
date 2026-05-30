---
name: accessibility-writing
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Rewrite and review reader-facing TEXT so it is accessible, understandable,
  inclusive, and safe to publish — alt text, plain-language copy, descriptive
  link text, accessible error messages, non-sensory instructions, inclusive
  wording, localization fit, and reading-burden estimates — and returns the
  clean copy separate from a validation table of assumptions, evidence, and
  not-verified items. [EXPLICIT]
  Use when the deliverable is the WORDS: image descriptions, UI microcopy,
  docs, onboarding, disclosures, form errors, CTAs, or an inclusive-language
  pass over existing text.
  Do NOT use for runtime/automated checks (axe, keyboard, screen-reader,
  contrast → accessibility-testing), for component behavior, focus order, or
  ARIA markup (→ accessibility-design), for WCAG governance evidence
  (→ accessibility-audit), or for persuasion/brand campaign copy
  (→ copywriting / brand-voice).
  Trigger: "accessibility writing", "accessible copy", "alt text",
  "plain language", "inclusive language", "reading level", "descriptive links",
  "accessible error message", "rewrite for accessibility"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
---
# Accessibility Writing

> Accessible writing helps more people understand, decide, recover, and act.

## TL;DR

Use this skill to turn copy, UI text, docs, image descriptions, error messages, and instructions into accessible writing. It produces clean reader-facing copy plus a separate validation note with assumptions, evidence, unresolved questions, and not-verified items. Do not invent visual details, reading-level measurements, audience facts, legal claims, or cultural context. [EXPLICIT]

## When this skill owns the work (and when it hands off)

| Signal in the request | Owns it here? | If not, route to |
|---|---|---|
| "Write/fix the wording, alt text, error text, link text" | Yes | — |
| "Make this readable / plain language / inclusive" | Yes | — |
| "Run axe / test keyboard / check contrast / screen reader" | No | `accessibility-testing` |
| "Fix focus order / ARIA roles / component behavior" | No | `accessibility-design` |
| "Produce WCAG conformance evidence / audit report" | No | `accessibility-audit` |
| "Make it punchier / on-brand / persuasive" (no a11y goal) | No | `copywriting` / `brand-voice` |

If a request mixes copy work with a handoff item (e.g. "rewrite errors AND test them"), do the copy here and explicitly name the follow-up skill for the rest.

## Output contract

Always return two clearly separated blocks, in this order:

1. **Reader-facing copy** — publish-ready, no evidence tags, no `not verified` markers inline.
2. **Validation table** — one row per changed item: `Item | Issue | Rewrite | Rationale | Evidence/Source | Assumption | Residual risk`.

Then a one-line **confidence** statement, capped by source completeness (missing image/chart/locale/measurement lowers it).

## Procedure

### Step 1: Discover
- Identify the content type: alt text, UI microcopy, docs, instructions, error copy, link text, localization, or inclusive language review.
- Capture audience, language/locale, channel, brand constraints, reading-level target, and publication risk.
- Inventory assets and source context: image, chart data, screenshot, original text, destination URL, product terminology, code/API names, legal or regulated copy.
- Mark missing inputs as `not verified`; for images or charts, do not infer details that are not visible or provided.

### Step 2: Analyze
- Classify each content item by job-to-be-done: inform, instruct, warn, recover, compare, navigate, or describe.
- For images, choose the right treatment: decorative empty alt, informative alt, functional alt, complex description, caption, or adjacent long description.
- For copy, check plain language, scannability, reading burden, inclusive wording, sensory-only instructions, link purpose, error recovery, and localization fit.
- Separate reader-facing copy from validation evidence so the final text remains usable.

### Step 3: Execute
- Produce accessible rewrites that preserve meaning, reduce jargon, define necessary acronyms, and keep one main idea per sentence or step.
- Write descriptive link text that makes sense out of context and distinguishes repeated links.
- Write error copy with the problem, likely cause when known, recovery action, and non-blaming tone.
- Replace sensory-only or positional instructions with names, labels, roles, headings, or stable identifiers.
- For inclusive language, propose contextual alternatives without silently changing code identifiers, product names, legal terms, or quoted source text.
- If writing to files, do so only when the user explicitly asks for an artifact or patch.

### Step 4: Validate
- Confirm reader-facing copy is clear without internal evidence tags unless the user requested inline annotation.
- Provide a validation table with changed item, issue, rewrite, rationale, evidence/source, assumption, and residual risk.
- Label reading level as measured only if a tool or user-provided measurement was actually used; otherwise mark it as an estimate.
- Reject keyword stuffing, invented image details, unsupported accessibility claims, and edits that erase necessary precision.

## Quality Criteria
- [ ] Audience, locale, channel, and content type are explicit or marked `not verified`.
- [ ] Alt text decisions distinguish decorative, informative, functional, complex, and missing-context assets.
- [ ] Plain-language rewrites preserve meaning while reducing unnecessary jargon, passive voice, dense sentences, and unexplained acronyms.
- [ ] Link text, headings, instructions, and errors are specific enough to be understood out of context.
- [ ] Inclusive language changes are contextual and do not silently rename code, APIs, product terms, or quoted text.
- [ ] Reading-level claims are measured or explicitly labeled as estimates.
- [ ] Reader-facing output is separated from evidence/validation notes.
- [ ] Every assumption, unverifiable detail, and requested-but-unsafe change is called out.

## Anti-Patterns

- Inventing image, chart, demographic, or product details to make alt text sound complete
- Stuffing SEO keywords into alt text at the expense of usefulness
- Making a text simpler by deleting critical warnings, constraints, or decision criteria
- Replacing technical terms that are required for the task without defining or preserving them
- Using only color, shape, size, or position to explain an action
- Claiming an exact reading level without measurement
- Putting evidence tags inside final user-facing copy by default

## Related Skills

- `accessibility-testing` — use for axe, keyboard, screen reader, contrast, and motion tests
- `accessibility-audit` — use for broader governance or WCAG audit evidence
- `accessibility-design` — use for component behavior, focus, ARIA, and visual interaction design
- `copywriting` or brand skills — use when persuasion or brand campaign copy is primary

## Usage

Example invocations:

- "/accessibility-writing" — Run the full accessibility writing workflow
- "Write alt text for these product images"
- "Rewrite this onboarding page in plain language"
- "Make this error copy accessible"
- "Review this document for inclusive language and reading burden"


## Assumptions & Limits

- Uses the language and locale of the input unless the user requests otherwise. [EXPLICIT]
- Assumes source text or asset context is available; missing image/chart data must be requested or marked `not verified`. [EXPLICIT]
- Does not certify legal, medical, financial, or regulatory wording; it can improve clarity and flag validation needs. [EXPLICIT]
- Does not replace `accessibility-testing` for runtime behavior, focus, screen reader, or contrast validation. [EXPLICIT]
- Does not mutate files unless the user explicitly asks for a patch or artifact. [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Image or chart missing | Ask for the asset/data or mark visual details `not verified`; do not hallucinate |
| Decorative image | Recommend empty alt and explain where the visual meaning is carried |
| Complex chart | Provide short alt plus long description structure using only supplied data |
| SEO conflicts with alt usefulness | Prioritize user-useful description and document the conflict |
| Reading level requested without measurement tool | Provide estimate and measurement recommendation, not a guaranteed score |
| Inclusive language conflicts with code/API/legal names | Preserve required terms, suggest aliases or explanatory copy |
| Sensory-only instruction | Rewrite using label, role, heading, or stable identifier |
