# Accessibility Writing — Body of Knowledge

## Canon

Accessible writing helps people understand content, navigate interfaces, recover from errors, and make decisions regardless of disability, reading context, language background, or cognitive load. The skill should produce reader-facing copy and a separate validation layer.

## Content Types

| Type | What good looks like | Common failure |
| --- | --- | --- |
| Alt text | Describes the purpose and useful visual information in context | Invents details, repeats surrounding text, or stuffs keywords |
| Decorative image | Empty alt or ignored by assistive tech when meaning is elsewhere | Adds noisy alt text for visual decoration |
| Functional image | Describes the action or destination, not the visual asset | Says "icon" instead of "Search" |
| Complex chart | Short alt plus adjacent long description from supplied data | Claims trends or values not present in the source |
| Plain-language copy | Uses familiar words, short sentences, active voice, and defined acronyms | Removes necessary precision or critical warnings |
| Link text | Names the destination or action out of context | "Click here", repeated "Learn more", or vague CTAs |
| Error copy | States what happened, how to fix it, and avoids blame | "Invalid", "Oops", or no recovery action |
| Instructions | Uses stable labels, roles, headings, and steps | Depends only on color, shape, position, or gesture |
| Inclusive language | Respects people-first/context-first wording and avoids unnecessary bias | Overwrites code/API/product names without warning |
| Localization | Adapts idioms, dates, currency, tone, and reading assumptions | Literal translation that changes meaning or excludes audience |

## Alt Text Decision Tree

1. If the image is decorative and repeats nearby meaning, recommend empty alt.
2. If the image is a control or link, describe the function.
3. If the image conveys information, describe the information needed for the task.
4. If the image is complex, provide short alt plus long description structure.
5. If the visual source or chart data is missing, ask for it or mark details `not verified`.

## Plain Language Rules

- Put the user's task first.
- Prefer common words unless a technical term is required.
- Define necessary acronyms on first use.
- Use active voice when the actor matters.
- Keep one main idea per sentence or step.
- Use headings and numbered steps for procedures.
- Preserve warnings, constraints, eligibility, legal meaning, and decision criteria.

## Inclusive Language Rules

- Replace unnecessary biased idioms and dehumanizing labels.
- Do not silently change identifiers, code names, product names, legal terms, or quoted text.
- Explain the tradeoff when inclusive language conflicts with brand, SEO, localization, or technical precision.
- Avoid euphemisms that reduce clarity.

## Reading-Level Claims

Reading level is a measurable claim only when a tool, metric, or provided score was used. Without measurement, say "estimated reading burden" and describe the observable changes: shorter sentences, fewer acronyms, clearer structure, and reduced jargon.

## Quality Metrics
| Metric | Target | How to Measure |
|--------|--------|---------------|
| Meaning preservation | 100% | Rewrite keeps source intent, warnings, constraints, and required terms |
| Asset honesty | 100% | No visual/chart detail is invented |
| Reader-facing clarity | 100% | Final copy can stand without internal evidence tags |
| Actionability | 100% | Errors, links, and instructions tell the user what to do next |
| Evidence coverage | 100% | Assumptions and not-verified items are explicit |
| Boundary control | 100% | Runtime testing/design/compliance work is routed to related skills |

## References
- User-supplied source text, screenshots, images, chart data, brand terms, and locale.
- Project terminology, code/API names, legal copy, and product constraints when provided.
- Measured readability outputs only when an actual tool or supplied score is available.
