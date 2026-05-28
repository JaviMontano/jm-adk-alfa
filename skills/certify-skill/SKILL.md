---
name: certify-skill
description: 
  This skill should be used when the user asks to "certify a skill",
  "validate this skill", "is this skill ready", "check skill quality",
  "grade this skill", or "run quality gate". Runs every quality check
  on a skill directory — structural validation, content audit, systemic
  coherence, and 10-criterion rubric scoring — then produces a
  certification report with pass/fail per checkpoint and a final
  certification level (CERTIFIED / CONDITIONAL / BLOCKED). Use this
  skill after running surgeon-skill to verify improvements, or standalone
  to assess any skill's production readiness, even if the user just says
  "is this good enough to ship". [EXPLICIT]
argument-hint: "path-to-skill-directory"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
model: opus
context: fork
version: 1.0.0
---

# Skill Certify

Final quality gate for Claude Code skills. Runs every check and produces a certification report that says exactly what passed, what failed, and what to fix — with no ambiguity about production readiness. [EXPLICIT]

Part of the Skill Quality Suite: x-ray-skill → surgeon-skill → **certify-skill** (+ trigger-skill, benchmark-skill, assembly-skill). Each skill is standalone. Use assembly-skill to run the full pipeline in one command. [EXPLICIT]

## Difference from x-ray-skill

x-ray-skill produces a diagnostic for exploration ("what's the state of this skill?"). certify-skill produces a verdict for decision-making ("can I ship this?"). The checks overlap, but the output differs:

| Aspect | x-ray-skill | certify-skill |
|--------|-------------|---------------|
| Output | Scorecard + gap analysis | Certification report + verdict |
| Tone | Descriptive (this IS the state) | Prescriptive (this PASSES or FAILS) |
| Actionability | "Top 5 issues" | "Fix these N blockers to certify" |
| Use case | Before improvement | After improvement (or standalone quality gate) |

## Usage

```
/certify-skill /path/to/skill-directory
/certify-skill ./my-skill
```

Parse the argument as the path to a skill directory containing SKILL.md. [EXPLICIT]

## The Certification Process

Read `references/certification-checklist.md` for the complete checklist with verification methods and the report template. [EXPLICIT]

### Phase 1: Structural Validation (automated)

Verify the skill's file structure mechanically. Structural failures block all further evaluation. [EXPLICIT]

```bash
ls {path}/SKILL.md                                      # S1: exists?
wc -l {path}/SKILL.md                                   # S2: under 500 lines?
# Parse YAML frontmatter between --- markers             # S3-S5
grep -oP '`[^`]*\.(md|py|json|html)`' {path}/SKILL.md   # S6: grep paths → ls each
ls -R {path}/ | grep -v SKILL.md                         # S7: list all files → check each referenced
python3 -m json.tool {path}/evals/evals.json 2>/dev/null # S8: valid JSON?
grep -r 'references/\|tools/' {path}                      # S9: no old paths?
```

**Abort condition:** If S1 fails (no SKILL.md), report BLOCKED immediately. No further phases.

Record each check as PASS/FAIL with the command output as evidence. 9 structural checks total — see `references/certification-checklist.md` for full definitions. [EXPLICIT]

### Phase 2: Content Validation (judgment required)

Read SKILL.md and evaluate content against 18 checks across 3 categories:

**2A: Frontmatter Quality (4 checks: F1-F4)**

| Check | What to Look For | Common Failure |
|-------|-----------------|----------------|
| F1: Third person | "This skill should be used when..." | First person ("I analyze...") |
| F2: 3-5 trigger phrases | Quoted phrases in description | Generic description with no triggers |
| F3: Pushy context | "even if they don't explicitly ask..." | Description stops at literal triggers |
| F4: Minimal allowed-tools | Only tools the skill actually uses | All tools listed when only Read+Grep needed |

**2B: Body Sections (9 checks: B1-B9)**

For each: is it present, substantive (not placeholder), and meets its minimum criteria? A section header with "TBD" scores as MISSING. [EXPLICIT]

| Check | Minimum Criteria | Why It Matters |
|-------|-----------------|----------------|
| B1: Title + value prop | 1-2 sentences answering "why does this exist?" | Without motivation, skill feels arbitrary |
| B2: Usage/activation | 2+ invocation examples | User doesn't know how to trigger it |
| B3: Progressive disclosure | Each ref mapped to load/skip conditions | Loads everything (waste) or nothing (miss) |
| B4: Core process | Actionable instructions, tables > bullets | The skill's purpose — without this, nothing works |
| B5: Assumptions & Limits | 3+ specific limits with handling | Silent failures on edge inputs |
| B6: Edge Cases | 3+ scenarios with handling instructions | Breaks on real-world variation |
| B7: Good vs Bad example | Side-by-side with reasoning | Model can't calibrate quality without reference points |
| B8: Validation Gate | 5+ testable checkboxes | No self-check → garbage passes through |
| B9: Reference Files | Table: file + content + load-when | Claude doesn't know files it wasn't told about |

**2C: Writing Quality (5 checks: W1-W5)**

| Check | Detection | Threshold |
|-------|-----------|-----------|
| W1: Imperative form | `grep -c 'you should\|you can\|you need' SKILL.md` | 0 occurrences |
| W2: No CAPS emphasis | Grep ALL CAPS words (excluding acronyms like API, JSON) | 0 occurrences |
| W3: Tables for structured data | Count tables vs bullet lists for multi-dim data | Tables >= bullets |
| W4: Code blocks for templates | Output formats in code blocks, not prose | All templates in blocks |
| W5: One concern per section | No section mixing process + examples + edge cases | No multi-topic sections |

### Phase 3: Systemic Coherence (multi-file only)

Skip for single-file skills — report N/A. For multi-file skills, run 5 checks:

| Check | Method | Pass Criteria | Severity |
|-------|--------|---------------|----------|
| C1: Terminology | Grep 5 key terms across files | Zero variants (same concept = same word) | HIGH |
| C2: No duplication | Spot-check 3 reference paragraphs against SKILL.md | No verbatim matches beyond 1-sentence pointers | MEDIUM |
| C3: Evidence taxonomy | Check if all files use the same claim-tagging system | One system everywhere | MEDIUM |
| C4: Schema alignment | Compare SKILL.md output template fields to workflow/eval JSON fields | Field names match exactly | HIGH |
| C5: Lean integration | Reference file pipeline sections are 3-5 lines, not re-explanations | Pointers, not prose | LOW |

### Phase 4: Quality Rubric (10 dimensions)

Score each dimension 1-10 using the detailed rubric in `references/certification-checklist.md` (which references x-ray-skill's `quality-rubric.md` for full scoring guides when available). [EXPLICIT]

For each dimension, provide:
1. **Numeric score** (1-10)
2. **One-sentence justification** citing a specific finding (not "good quality" — name the evidence)
3. **If score < 7:** specific fix required to reach 7, with estimated effort

**Scoring discipline:** A score without evidence is invalid. "Clarity: 8" is not a finding. "Clarity: 8 — all terms defined in Glossary section, zero ambiguous pronouns found" is a finding.

### Phase 5: MOAT Validation (deterministic)

If Phases 1-4 result in CERTIFIED, run 5 additional deterministic checks from `references/certification-checklist.md` Phase 5:

| Check | Pass Criteria |
|-------|---------------|
| M1: evals/evals.json exists with >= 5 tests | File present, >= 5 distinct entries |
| M2: false-positive + edge-case evals | >= 1 of each type in evals.json |
| M3: references/ files substantive | All >= 20 lines, zero TBD/TODO/placeholder |
| M4: Template A structure | "## Usage" or "## When to Activate" + "## Validation Gate" present; no Template B markers |
| M5: evidence tag coverage | [EXPLICIT]/[INFERRED]/[OPEN] on >= 80% factual claims (>= 50% for Utility tier) |

Skip Phase 5 if the skill is CONDITIONAL or BLOCKED — MOAT requires CERTIFIED as a prerequisite. [EXPLICIT]

### Phase 6: Produce Report

Use the Certification Report Template from `references/certification-checklist.md`. Apply the certification formula:

| Level | Formula | Recommendation |
|-------|---------|---------------|
| **MOAT** | CERTIFIED + all M1-M5 pass | "Ship it. Production-quality with full quality assurance." |
| **CERTIFIED** | All dimensions >= 7, average >= 8, all structural pass | "Passes quality. Upgrade to MOAT: add {missing M-checks}." |
| **CONDITIONAL** | Average >= 8 but 1-2 dims at 6, or 1-2 structural failures | "Fix {N} blockers, re-certify. Effort: {estimate}." |
| **BLOCKED** | Any dim < 6, or 3+ structural failures, or no SKILL.md | "Run `/surgeon-skill {path}`. {N} foundational issues." |

**Certification is deterministic for structural checks and MOAT M-checks, judgment-based for rubric.** If two certifications of the same unchanged skill produce different verdicts, the structural and MOAT results should be identical — only rubric scores may vary by 1 point on subjective dimensions (density, simplicity, value).

## Assumptions & Limits

- Read-only. This skill never modifies the skill being certified.
- Structural checks (Phase 1) are deterministic — same skill always produces same results.
- Rubric dimensions 4 (density), 5 (simplicity), and 10 (value) involve subjective judgment. Expected variance: 1 point per run. If variance exceeds 2 points, the skill's quality is in a borderline zone.
- Cannot evaluate runtime behavior. A skill can pass certification structurally but produce poor output due to flawed instruction logic. Use the skill-creator's eval loop for behavioral testing.
- Systemic coherence (Phase 3) is N/A for single-file skills. This is correct, not a gap.
- Certification takes 5-15 minutes depending on file count. Skills with 10+ files increase Phase 3 check time linearly.

### Failure Modes

| Failure | Signal | Recovery |
|---------|--------|----------|
| No SKILL.md found | S1 fails | Report BLOCKED immediately. Ask user to verify path. |
| Unparseable frontmatter | YAML error on frontmatter parse | Report as BLOCKER. Skill cannot trigger without valid frontmatter. |
| Borderline scores (multiple 7s, average 7.9) | CONDITIONAL but close to BLOCKED | Report honestly. List which dimensions need +1 to reach CERTIFIED. |
| Prior certification exists | User asks to re-certify after changes | Show delta: improved/degraded/unchanged per dimension. Highlight what changed. |
| Skill deliberately breaks conventions | Intentional deviation documented in the skill | Flag but don't auto-fail. Note: "Intentional deviation — user decision." |

## Edge Cases

- **Skill with no frontmatter:** BLOCKED. Primary fix: "Add YAML frontmatter with name and description between --- markers."
- **Skill that deliberately breaks conventions:** Note the deviation. If documented and intentional, flag but don't auto-fail. If undocumented, score as a gap.
- **Re-certification after surgeon-skill:** Show before/after delta. Highlight improvements. If new issues appeared (rare), flag them explicitly.
- **Very large skill (10+ files):** Increase Phase 3 sample size. Check 5 paragraphs instead of 3. Check all key terms instead of 5.
- **Skill that scores exactly on thresholds:** Average 8.0, all dims exactly 7 = CERTIFIED. Average 7.9 = CONDITIONAL (formula is strict). Document the edge clearly.
- **Single-file skill scoring 10/10:** Valid. A well-crafted single SKILL.md with no need for references/scripts/agents can score perfectly. Don't penalize simplicity.

## Example: Good vs Bad Certification

**Bad certification:**
```
Certification: CONDITIONAL. Some issues found. Please fix and re-certify. [EXPLICIT]
```
No evidence, no specifics, no fix instructions. Useless. [EXPLICIT]

**Good certification:**
```
Certification: CONDITIONAL (11/13 gate, avg 7.8/10)
Fails: S6 (references/patterns.md referenced but file doesn't exist),
       Checkpoint 6 (no Good vs Bad example). [EXPLICIT]
Rubric: Depth 6/10 (only 2 edge cases; need 3+), others 8+. [EXPLICIT]
Fix: (1) Create references/patterns.md or remove the reference. [EXPLICIT]
     (2) Add Good vs Bad section with concrete comparison. [EXPLICIT]
     (3) Add 1+ edge case to Edge Cases section. [EXPLICIT]
Estimated effort: 30 minutes. Re-certify after. [EXPLICIT]
```
Specific, evidenced, actionable, with effort estimate. [EXPLICIT]

## Validation Gate

Before delivering the certification report:

- [ ] All 9 structural checks have a binary PASS/FAIL with command evidence
- [ ] All 18 content checks (F1-4, B1-9, W1-5) have a result
- [ ] Systemic checks completed or N/A (with reason) for single-file skills
- [ ] All 10 rubric dimensions have a numeric score + one-sentence justification with evidence
- [ ] MOAT checks M1-M5 evaluated (or skipped if not CERTIFIED)
- [ ] Certification level matches the formula exactly (not assigned by feel)
- [ ] Every FAIL or BLOCKED item has a specific fix with estimated effort
- [ ] Report follows the template from references/certification-checklist.md
- [ ] If re-certification: delta from prior run is shown

## Reference Files

| File | Content | Load When |
|------|---------|-----------|
| `references/certification-checklist.md` | Complete checklist: 9 structural checks with commands, 18 content checks with criteria, 5 systemic checks with methods, 10 rubric scoring summaries, certification formula, report template | Always — this IS the certification engine |

---
**Author:** Javier Montano | **Last updated:** March 27, 2026
