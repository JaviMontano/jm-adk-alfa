---
name: auto-prompt-matching
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Deterministically route a user request to the best available skill or prompt by
  reading canonical indexes, scoring explicit trigger/purpose matches, resolving
  ties with stable rules, and emitting an auditable routing decision. [EXPLICIT]
  Trigger: "auto prompt matching", "route this prompt", "which skill should handle",
  "match user intent", "prompt routing"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Auto Prompt Matching

> "Method over hacks. Evidence over assumption."

## TL;DR

Routes user input to the best available skill or prompt using deterministic evidence from `PRISTINO-INDEX.md`, `.agent/skills_index.json`, skill frontmatter, prompt metadata, and explicit user prefixes. Use for orchestration-layer prompt routing, not for executing the routed task. Never invent a skill, prompt, confidence score, or capability that is not present in the inspected sources. [EXPLICIT]

## Procedure

### Step 1: Discover
- Capture the raw user request, explicit prefixes, mentioned brand/context, requested artifact type, language, and safety constraints.
- Load the smallest sufficient routing sources in this order: explicit prefix/command, `PRISTINO-INDEX.md`, `.agent/skills_index.json`, matching `skills/*/SKILL.md`, and relevant prompt metadata.
- Normalize tokens deterministically: lowercase, strip punctuation, split hyphenated slugs, preserve quoted terms, and keep brand names as exact terms.
- Build a candidate list only from discovered skills/prompts. Mark missing indexes as `coverage_gap`; do not replace them with memory.

### Step 2: Analyze
- Score candidates with the stable rubric in `assets/routing-checklist.md`: explicit trigger, slug/name match, purpose match, artifact type, context/brand fit, negative-scope penalties, and source freshness.
- Keep the top three candidates with evidence for each score component.
- Apply stable tie-breakers: explicit prefix wins; then exact trigger; then exact slug/name; then stronger purpose evidence; then narrower scope; then alphabetical slug for reproducibility.
- Classify confidence as `route`, `ask`, or `decline` using the checklist thresholds. Do not force a route when the evidence is ambiguous.

### Step 3: Execute
- Return a routing decision, not the downstream task result.
- Include selected skill/prompt, confidence band, score components, sources inspected, rejected alternatives, and required next action.
- If no candidate is reliable, ask a targeted clarification or hand off to discovery/orchestration instead of guessing.
- Use evidence tags on all claims: `[CÓDIGO]` for inspected repo/index evidence, `[CONFIG]` for routing policy, `[INFERENCIA]` for derived fit, and `[SUPUESTO]` only for user-accepted defaults.

### Step 4: Validate
- Verify the selected route exists in the inspected index or file tree.
- Verify all confidence and tie-break claims cite score components.
- Verify false positives are rejected: weather, generic writing, unsupported plugin claims, or requests outside the indexed corpus.
- Verify `assets/routing-checklist.md` was applied before finalizing the route.

## Quality Criteria

- [ ] Evidence tags applied to every routing claim
- [ ] Sources inspected are listed with path or index name
- [ ] Candidate set contains only discovered skills/prompts
- [ ] Score components and tie-breakers are visible
- [ ] Ambiguous cases return `ask` with a narrow clarification
- [ ] Unsupported cases return `decline` or handoff without invented capabilities
- [ ] Final decision references `assets/routing-checklist.md`
- [ ] Output is actionable by the coordinator

## Related Skills

- `input-analyst` - normalize messy user input before routing
- `workflow-orchestration` - plan resumable multi-step execution after routing
- `subagent-orchestration` - isolate candidate reviewers when routing risk is high
- `output-contract-enforcer` - enforce downstream deliverable shape after routing

## Usage

Example invocations:

- "/auto-prompt-matching" - Run the full routing workflow
- "Which skill should handle this prompt: build a deterministic XLSX template?"
- "Route this user request to the right prompt without executing it."


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Uses the language of the user request unless repo conventions require otherwise [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Does not execute the routed skill unless the user explicitly asks for execution after routing [EXPLICIT]
- Does not use memory or unstated plugin knowledge as a source of truth when indexes are unavailable [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Ask for the task goal and artifact type before routing |
| Explicit prefix names a valid skill | Route to that skill and still report source evidence |
| Multiple high-confidence matches | Apply tie-breakers; if still tied, ask one narrow clarification |
| Source index missing or stale | Report `coverage_gap` and inspect direct skill files where possible |
| Unsupported capability | Decline or hand off; do not invent a skill |
| Out-of-scope request | Redirect to discovery/orchestration or ask for scope |

## Assets

- `assets/routing-checklist.md` defines the scoring, tie-break, and final decision checklist.
