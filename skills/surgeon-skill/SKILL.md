---
name: surgeon-skill
description: 
  This skill should be used when the user asks to "improve a skill",
  "fix this skill", "upgrade skill quality", "apply improvements",
  "make this skill production-ready", or "elevate this skill". [EXPLICIT]
  Reads a skill directory, identifies the highest-impact improvements,
  and applies them systematically — preserving 100% of domain content
  while upgrading structural infrastructure, instructional quality,
  and developer experience. Use this skill whenever someone has an
  x-ray-skill report and wants to act on it, or when they point to a
  skill directory and say "make it better". [EXPLICIT]
argument-hint: "path-to-skill-directory"
model: opus
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
model: opus
version: 1.0.0
---

# Skill Surgeon

Precision improvements for Claude Code skills. Identifies fixes prioritized by impact, applies each with snapshot verification, and produces a changelog — so domain content is never lost and every change is justified. [EXPLICIT]

Part of the Skill Quality Suite: x-ray-skill → **surgeon-skill** → certify-skill (+ trigger-skill, benchmark-skill, assembly-skill). Each skill is standalone. Use assembly-skill to run the full pipeline in one command. [EXPLICIT]

## Usage

```
/surgeon-skill /path/to/skill-directory
/surgeon-skill ./my-skill
```

Parse the argument as the path to a skill directory containing SKILL.md. If an x-ray-skill report exists in the conversation, use its scorecard to prioritize. Otherwise, run an internal diagnostic first. [EXPLICIT]

## The Improvement Process

### Step 1: Assess Current State

**If x-ray-skill report is available:** Use its scorecard, top 5 issues, and component classification directly. Skip to Step 2.

**If no report:** Perform a quick assessment:

1. Read SKILL.md completely. Record line count. [EXPLICIT]
2. `Glob <path>/**/*` — list all files, note directory structure. [EXPLICIT]
3. Parse frontmatter — check name (kebab-case?), description (3rd person? triggers?), allowed-tools. [EXPLICIT]
4. Scan for missing gold-standard components: references/, evals/, progressive disclosure section, Good vs Bad example, Validation Gate. [EXPLICIT]
5. Estimate current rubric score: below 6 (BLOCKED), 6-7 (needs work), 7-8 (polish), 8+ (minor tweaks). [EXPLICIT]

**Decision: scope of intervention.** The assessment determines how many layers to apply:
- Score < 6: Focus on Layer A only — structural fixes unblock everything else
- Score 6-7: Layers A + B — infrastructure + instructional quality
- Score 7-8: Layers B + C — content polish + developer experience
- Score 8+: Layer C only — minor refinements, or report "no intervention needed"

### Step 2: Plan Interventions

Read `references/improvement-patterns.md` for the complete pattern library (15 patterns across 3 layers). Match patterns to assessment findings:

| Priority | Layer | What It Fixes | Patterns |
|----------|-------|---------------|----------|
| 1 | **A: Infrastructure** | Structure that blocks all other quality | A1 Frontmatter, A2 Directory naming, A3 Progressive disclosure, A4 Evals, A5 Glossary/contracts |
| 2 | **B: Content** | How well instructions guide the model | B1 Good/Bad example, B2 Caps→reasoning, B3 Reference pointers, B4 Failure modes, B5 Evidence tagging |
| 3 | **C: DX** | Maintainability and iteration ease | C1 Deduplication, C2 Confidence aggregation, C3 Backtrack protocol, C4 Multi-turn, C5 Schema alignment |

**Only select patterns where the assessment found a gap.** Do not apply all 15 patterns to every skill — a simple utility skill doesn't need C2 (confidence aggregation) or C4 (multi-turn handling).

Present the plan before executing:

```
Plan: {N} interventions across {M} layers. [EXPLICIT]
Layer A: {A1: fix description triggers, A3: add Before Analysis section}
Layer B: {B1: add Good vs Bad example, B4: add Failure Modes table}
Layer C: {C1: deduplicate workflow}
Estimated score improvement: {current} → {projected}
Proceed?
```

**Wait for user confirmation before modifying any file.** The plan is a proposal, not an execution order.

### Step 3: Execute Interventions

For each intervention, follow the Snapshot-Apply-Verify-Document protocol:

| Phase | Action | Failure Mode | Recovery |
|-------|--------|-------------|----------|
| **Snapshot** | Read the target file completely. Store key sections mentally. | File not found | Check path; may be in a subdirectory |
| **Apply** | Make the specific change using Edit (prefer) or Write (for new files) | Edit fails (old_string not unique) | Expand the match context or use Write for full rewrites |
| **Verify** | Re-read the modified file. Confirm every domain concept from the snapshot is still present. | Domain content missing | Undo the change. Try a different approach that preserves the content. |
| **Document** | Record: what changed, why, which file, lines affected | Forgot to document | Review git diff or re-read the file to reconstruct |

**Execution order:** All Layer A interventions first (in numbered order), then B, then C. Within each layer, numbered order (A1→A2→A3...) because later patterns may depend on earlier structural fixes.

**Key trade-off: depth vs breadth.** Applying 5 patterns thoroughly (with verification) produces better results than 15 patterns superficially. If time/context is limited, prioritize fewer interventions done completely over many done partially.

### Step 4: Apply Writing Rules

After structural fixes, audit the prose. Read `references/writing-rules.md` for the full guide. Key checks:

| Check | Detection | Fix |
|-------|-----------|-----|
| Second person | Grep "you should", "you can", "you need" | Rewrite in imperative: "Read...", "Parse..." |
| CAPS emphasis | Grep words in ALL CAPS (excluding acronyms) | Replace with reasoning: "because X" |
| Bullets where tables belong | Structured data (2+ dimensions) in bullet form | Convert to table |
| Prose where code blocks belong | Output format described in words | Show exact template in code block |
| Unreferenced files | File in references/ not mentioned in SKILL.md | Add reference pointer with WHEN condition |
| Term inconsistency | Same concept, different words across files | Standardize on SKILL.md's terminology |

**When to skip Step 4:** If the skill scored 8+ on the quality rubric's clarity and simplicity dimensions, prose is already strong. Focus effort elsewhere.

### Step 5: Produce Changelog

Structured changelog documenting every change:

```markdown
## Changelog: {skill-name}

### Layer A: Infrastructure
| # | Pattern | Change | File(s) | Justification |
|---|---------|--------|---------|---------------|
| A1 | Frontmatter | Rewrote description: added 5 triggers, 3rd person, pushy context | SKILL.md:1-12 | Was first-person with no triggers; skill under-triggering |
| A3 | Progressive disclosure | Added "Before Analysis" section with 4 reference loading conditions | SKILL.md:38-47 | References existed but Claude didn't know when to load them |

### Layer B: Content
| # | Pattern | Change | File(s) | Justification |
|---|---------|--------|---------|---------------|
| B1 | Good/Bad | Added example section with concrete comparison | SKILL.md:196-211 | No calibration signal; model couldn't distinguish quality |

### Layer C: DX
(none applied — skill is single-file)

### Summary
- Files created: {N}
- Files modified: {N}
- Files reorganized: {N}
- Files deleted: 0
- Domain content preserved: 100% (verified by re-reading each modified file)
- Estimated score: {before} → {after}
```

## Content Preservation Protocol

The surgeon-skill's inviolable constraint. Every other design decision is negotiable; this one is not. [EXPLICIT]

| Rule | Meaning | Test |
|------|---------|------|
| Never delete domain content | Methodology descriptions, protocol steps, domain examples, decision frameworks | After each change: can every original concept be found? |
| Reorganize freely | Move between files, restructure sections, consolidate | Content exists somewhere in the skill — it may have moved |
| Enrich from existing signals | Add edge cases, failure modes, trade-offs implicit in the original content | New content traces to something already stated or implied |
| Flag before removing | If content seems redundant, verify both copies add unique value | Diff the two occurrences — if truly identical, keep the more specific one |
| Never invent domain content | Adding requirements the user didn't express or imply is scope invention, not improvement | Every added sentence answers: "where in the original skill does this idea originate?" |

**Why this matters:** Skills encode domain expertise accumulated over time. Structural improvements are valuable, but they must not erase the knowledge that makes the skill useful. A beautifully structured skill with diluted domain content is worse than a messy skill with rich knowledge.

## Assumptions & Limits

- This skill modifies files. It requires Write and Edit permissions and asks for user confirmation before executing the plan.
- Cannot improve skills with side effects (deploy, commit, push) without understanding the blast radius — flag these for manual review.
- Content quality improvements (writing style, example selection) involve judgment. The writing rules in `references/writing-rules.md` are guidelines, not laws — the user may prefer different conventions.
- Does not run evals or test runtime behavior. Use the skill-creator's eval loop for behavioral testing after structural improvements.
- Complex multi-agent skills: the surgeon improves each file independently. It may not fully understand inter-agent coordination logic — flag suspected coordination issues for user review.
- Maximum effective scope: ~15 files per session. Beyond that, context pressure degrades verification quality. For very large skills, run in multiple sessions (Layer A in session 1, Layer B in session 2).

### Failure Modes

| Failure | Signal | Recovery |
|---------|--------|----------|
| Edit fails (non-unique old_string) | Tool error message | Expand match context to make old_string unique, or use Write for a full rewrite |
| Domain content lost after intervention | Verification step finds missing concept | Undo the change. Re-read the snapshot. Try a minimal edit instead of a rewrite. |
| Plan too ambitious for context window | 15+ interventions planned | Prioritize: apply top 5 highest-impact patterns this session. Defer the rest. |
| User rejects the plan | "Don't change X" or "Skip Y" | Remove the rejected interventions. Re-present the trimmed plan. |
| Skill has no SKILL.md | Cannot find the file | Not a skill directory. Ask user to verify the path. |
| Writing rules conflict with user's style | User's existing skill uses different conventions | Respect the user's established patterns. Note the deviation in the changelog. |

## Edge Cases

- **Skill with no obvious issues:** Report "no intervention needed" with the current estimated score. Do not invent improvements to justify the skill's existence.
- **Massive skill (2000+ lines in SKILL.md):** Primary intervention is progressive disclosure: extract content to references/. Decide what to extract by identifying sections that are needed <50% of the time.
- **Skill in a language other than English:** Apply structural patterns (frontmatter, directories, evals) regardless of language. Apply writing rules in the skill's language — don't translate.
- **Skill with uncommitted changes:** Warn before modifying. The user should commit or stash first to preserve a rollback point.
- **Skill that x-ray-skill scored as CERTIFIED:** No intervention needed unless the user specifically requests refinement. Report: "Skill meets production standards. Specific refinement requests welcome."
- **Conflicting patterns:** A3 (progressive disclosure) may conflict with density goals if it splits content too aggressively. Prefer keeping related content together unless the 500-line ceiling forces extraction.

## Example: Good vs Bad Intervention

**Bad intervention:**
```
Applied B2 (caps→reasoning). Changed 12 lines. (No snapshot, no verification, no changelog.)
```
No evidence of content preservation. No justification. No traceability. [EXPLICIT]

**Good intervention:**
```
Snapshot: Read SKILL.md lines 49-50. Content: "ALWAYS preserve intent. NEVER change meaning."
Applied B2: Replaced with "Preserve intent when correcting. Surface corrections change spelling,
not meaning — a wrong correction is worse than leaving the typo."
Verified: Same two concepts (intent preservation, meaning preservation) present. Added reasoning
(wrong correction > leaving typo) derived from the original "NEVER change meaning" imperative. [EXPLICIT]
Justification: LLMs respond better to reasoning than to commands. [EXPLICIT]
```

## Validation Gate

Before declaring improvements complete:

- [ ] Every intervention followed Snapshot-Apply-Verify-Document (no skipped phases)
- [ ] Zero domain content lost (verified by re-reading each modified file against snapshot)
- [ ] All new files are referenced from SKILL.md with loading conditions
- [ ] Cross-file terminology is consistent after all changes (grep 5 key terms)
- [ ] SKILL.md remains under 500 lines after all additions
- [ ] Changelog documents every change with file, lines, and justification
- [ ] User confirmed the plan before execution began

## Reference Files

| File | Content | Load When |
|------|---------|-----------|
| `references/improvement-patterns.md` | 15 patterns across 3 layers (A: infrastructure, B: content, C: DX) with When/Fix/Before→After for each | Step 2 — needed to select applicable patterns from the assessment |
| `references/writing-rules.md` | Style guide: voice (imperative, 3rd person), emphasis (WHY > CAPS), structure (tables > bullets), anti-patterns (6 common mistakes), cross-file consistency rules | Step 4 — needed when auditing prose quality after structural fixes |

---
**Author:** Javier Montano | **Last updated:** March 18, 2026
