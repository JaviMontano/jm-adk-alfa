---
name: x-ray-skill
description: 
  This skill should be used when the user asks to "audit a skill",
  "review skill quality", "diagnose a skill", "score this skill",
  "x-ray this skill", or "how good is this skill". Reads an entire
  skill directory and produces a structured diagnostic scorecard
  against the Anthropic gold standard — scoring 10 quality dimensions,
  running a 13-point validation gate, and checking systemic coherence
  across all files. Use this skill whenever someone wants to understand
  the quality state of a skill before improving it, even if they just
  say "check this skill" or provide a path to a skill directory. [EXPLICIT]
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

# Skill X-Ray

Diagnostic scan for Claude Code skills. Reads every file, scores against the gold standard, and produces a prioritized gap analysis — so you know exactly what to fix and in what order. [EXPLICIT]

Part of the Skill Quality Suite (6 skills):

| Skill | Role | Modifies Files? |
|-------|------|-----------------|
| **x-ray-skill** | Diagnostic scan + scorecard | No |
| surgeon-skill | Precision improvements | Yes |
| certify-skill | Final quality gate + verdict | No |
| trigger-skill | Description optimization | Yes (description only) |
| benchmark-skill | Before/after comparison | No |
| assembly-skill | One-command full pipeline | Yes (delegates) |

Each skill is standalone. Use assembly-skill to run the full pipeline in one command. [EXPLICIT]

## Usage

```
/x-ray-skill /path/to/skill-directory
/x-ray-skill ./my-skill
/x-ray-skill ~/.claude/skills/some-skill
```

Parse the argument as the path to a skill directory containing SKILL.md. If the path points to a .skill ZIP file, extract it to a temp directory first. [EXPLICIT]

## The Diagnostic Process

### Step 1: Inventory

Read every file in the skill directory recursively:

```bash
Glob <path>/**/*
wc -l <each file>
```

For each file, record: path, line count, and type. Classify against `references/gold-standard-anatomy.md`:

| Component | Present? | Path | Lines | Status | Decision Rationale |
|-----------|----------|------|-------|--------|--------------------|
| SKILL.md | | | | | Required for all skills |
| references/ | | | | | Needed when SKILL.md > 300 lines or has deep domain content |
| scripts/ | | | | | Needed when deterministic tasks repeat across invocations |
| agents/ | | | | | Needed when sub-roles operate independently (not sequentially) |
| evals/evals.json | | | | | Needed when the skill will be iteratively improved |
| assets/ | | | | | Needed when the skill generates files from templates |

Status values:
- **PRESENT** — component exists
- **MISSING-CRITICAL** — gold standard requires it and its absence degrades the skill
- **MISSING-OPTIONAL** — gold standard recommends it but the skill functions without it
- **N/A** — not applicable for this skill type (explain why)

**Trade-off for "MISSING" decisions:** Distinguishing critical from optional requires understanding the skill's domain. A simple utility skill (string formatter) doesn't need agents/. A complex multi-phase skill (discovery orchestrator) without evals/ is a quality risk. Ground the status in the skill's complexity, not in a universal template.

### Step 2: Frontmatter Validation

Parse SKILL.md YAML frontmatter. Verify each field:

| Field | Value | Valid? | Issue | Severity |
|-------|-------|--------|-------|----------|
| name | | kebab-case, <=64 chars, no uppercase, no angle brackets? | | BLOCKER if invalid |
| description | | Third person? 3-5 trigger phrases? Pushy context? <=1024 chars? | | BLOCKER if missing triggers |
| argument-hint | | Present when skill takes arguments? Format documented? | | WARNING if missing |
| allowed-tools | | Minimum set? No over-permissioning? | | WARNING if over-broad |
| model | | Justified? (opus = complex reasoning, sonnet = default) | | INFO |
| context | | fork only when isolated subagent needed? | | INFO |

**Detection method for trigger quality:** Read the description aloud. If a colleague couldn't tell when to use this skill from the description alone, triggers are insufficient. Count quoted phrases — fewer than 3 is a gap.

### Step 3: Body Audit

Read SKILL.md body section by section. For each expected section:

| Section | Present? | Lines | Substantive? | Issue |
|---------|----------|-------|-------------|-------|
| Title + value proposition | | | 1-2 sentences explaining WHY? | |
| When to Activate / Usage | | | Concrete examples with arguments? | |
| Before {Action} (progressive disclosure) | | | Maps refs to conditions? | |
| Core Process | | | Tables > bullets? Actionable? | |
| Assumptions & Limits | | | Specific, not boilerplate? | |
| Edge Cases (3+) | | | Each with handling instruction? | |
| Good vs Bad example (1+) | | | Concrete comparison with reasoning? | |
| Antipatterns | | | Each with rationale? | |
| Validation Gate (5+ criteria) | | | Testable, not subjective? | |
| Reference Files | | | Table with file + content + load-when? | |

**"Substantive" means:** The section contains content that affects behavior. A section header with "TBD" or a single vague sentence is present but not substantive — score it as MISSING.

### Step 4: Quality Rubric Scoring

Read `references/quality-rubric.md` for the full scoring guide. Score each dimension using the detection methods described there. [EXPLICIT]

| # | Criterion | Score | Key Finding | Evidence |
|---|-----------|-------|-------------|----------|
| 1 | Foundation | /10 | | {cite specific line/section} |
| 2 | Truthfulness | /10 | | |
| 3 | Quality | /10 | | |
| 4 | Density | /10 | | |
| 5 | Simplicity | /10 | | |
| 6 | Clarity | /10 | | |
| 7 | Precision | /10 | | |
| 8 | Depth | /10 | | |
| 9 | Coherence | /10 | | |
| 10 | Value | /10 | | |
| | **Average** | **/10** | | |

**Scoring discipline:** Every score requires evidence. "Foundation: 8/10" without citing what's grounded and what isn't is not a valid score. The "Evidence" column prevents drive-by scoring.

**Scoring edge cases:**
- A skill that does one thing brilliantly but has no edge cases: high on clarity/precision, low on depth.
- A single-file skill: coherence gets N/A or automatic 10 (no cross-file to contradict).
- A skill with excellent prose but broken references: high on density/clarity, low on quality.

### Step 5: Meta-Validation Gate

Run the 13-point gate from `references/quality-rubric.md`. Each checkpoint is binary — no partial credit. [EXPLICIT]

| # | Checkpoint | Result | Evidence |
|---|-----------|--------|----------|
| 1 | One SKILL.md in top-level directory | | `ls` output |
| 2 | Frontmatter has name + description | | Parse result |
| 3 | Description: 3rd person, 3-5 triggers, pushy | | Quoted triggers |
| 4 | Body uses imperative form | | Grep count for "you should" |
| 5 | SKILL.md under 500 lines | | `wc -l` |
| 6 | 1+ Good vs Bad example | | Section name |
| 7 | Validation gate with 5+ criteria | | Checkbox count |
| 8 | Assumptions & Limits section, specific | | Section present + substantive |
| 9 | Edge Cases with 3+ scenarios | | Item count |
| 10 | All referenced files exist | | Grep paths + ls each |
| 11 | Progressive disclosure mechanism | | "Before" section exists |
| 12 | No security-compromising content | | Content review |
| 13 | Intent wouldn't surprise user | | Semantic review |

Gate result: **PASS** (13/13) / **CONDITIONAL** (11-12) / **BLOCKED** (<11)

### Step 6: Systemic Coherence (multi-file skills only)

Skip this step for single-file skills — report N/A. [EXPLICIT]

| Check | Method | Result | Severity |
|-------|--------|--------|----------|
| Terminology consistency | Pick 5 key terms from SKILL.md; grep each across all files | | HIGH if variants found |
| Cross-reference integrity | Grep file paths in SKILL.md → verify existence; list all files → verify each is referenced | | HIGH if orphans or broken refs |
| Evidence taxonomy | Check if claims are tagged consistently (explicit/inferred/open or equivalent) | | MEDIUM if mixed systems |
| Schema alignment | Compare output templates in SKILL.md to JSON schemas in workflow/evals | | HIGH if fields mismatch |
| Content duplication | Spot-check 3 paragraphs from reference files against SKILL.md | | MEDIUM if duplicated |
| Integration section weight | Reference files should have lean pipeline pointers (3-5 lines), not re-explanations | | LOW but signals bloat |

### Step 7: Produce Scorecard

Synthesize into the X-Ray Report. This is the only deliverable — every previous step is intermediate. [EXPLICIT]

```markdown
# X-Ray Report: {skill-name}

## Summary
- Overall score: {average}/10
- Gate: {PASS/CONDITIONAL/BLOCKED} ({N}/13)
- Certification readiness: {CERTIFIED/CONDITIONAL/BLOCKED}
- Files: {N} files, {N} total lines
- Skill type: {single-file / multi-file / plugin-embedded}

## Rubric Scores
| # | Criterion | Score | Key Finding |
|---|-----------|-------|-------------|
| 1-10 | ... | /10 | {one sentence with evidence} |
| | Average | /10 | |

## Gate Results
| # | Checkpoint | Result |
|---|-----------|--------|
| 1-13 | ... | PASS/FAIL |

## Top 5 Issues (prioritized by certification impact)
1. [{BLOCKER/WARNING}] {issue} — affects {criterion}, fix: {specific action}
2. ...

## Component Classification
| Component | Status | Tag |
|-----------|--------|-----|
| {file/dir} | {status} | FORTALEZA / GAP / DEBILIDAD / UNICO |

## Systemic Issues (if multi-file)
{coherence findings}

## Recommended Next Step
- BLOCKED → `/surgeon-skill {path}` — {N} foundational issues need resolution
- CONDITIONAL → Fix {specific 1-2 items} manually, then `/certify-skill {path}`
- CERTIFIED → No action needed. Skill meets production standards.
```

**Prioritization logic for Top 5:** BLOCKER gate failures first (they prevent certification), then lowest rubric scores (they drag the average below 8), then systemic issues (they compound across files). Each issue gets a severity tag and a specific action — never "improve quality."

## Assumptions & Limits

- Read-only. This skill never modifies the skill being analyzed.
- Scores are relative to the Anthropic gold standard. A score of 7 means "production-acceptable, ships today." A score of 5 means "functional but missing standard infrastructure." Below 4 indicates structural problems.
- Cannot evaluate runtime behavior. A skill can score 10/10 structurally but produce poor output due to flawed logic. Use the skill-creator's eval loop for behavioral testing.
- Systemic coherence checks require 2+ files. Single-file skills receive N/A on coherence — this is correct, not a gap.
- Subjective dimensions (value, simplicity, density) may vary by 1 point between runs. Structural dimensions (quality, precision, coherence) should be deterministic.
- The scoring takes 5-15 minutes depending on skill size. Skills with 10+ files take longer because cross-file checks scale linearly.

### Failure Modes

| Failure | Signal | Recovery |
|---------|--------|----------|
| SKILL.md not found at path | Glob returns no match | Ask user to verify path. Check for nested `skills/{name}/SKILL.md` in plugin structures. |
| Frontmatter not parseable | YAML parse error | Report as BLOCKER. The skill cannot trigger without valid frontmatter. |
| Skill is a .skill ZIP | File extension is .skill, not a directory | Extract to temp dir, analyze, note archive format in report. |
| Rubric score disagreement with prior run | Same skill, different scores | Expected for subjective dims (1-point variance). Flag if difference > 2 — likely a scoring inconsistency. |
| Massive skill (50+ files) | Glob returns many files | Prioritize: SKILL.md first, then evals, then references. Sample 5 reference files for cross-checks instead of all. |

## Edge Cases

- **Single-file skill (SKILL.md only):** Valid structure. Skip Step 6. Component classification shows references/, scripts/, agents/ as MISSING-OPTIONAL (not gaps unless skill complexity warrants them).
- **ZIP archive (.skill file):** Extract to temp directory. Run full analysis. Note "Source: .skill archive" in report header.
- **Draft skill (frontmatter + body, no sections):** Score body audit as mostly MISSING. Certification: BLOCKED. Recommendation: "Run /surgeon-skill to add standard sections."
- **Skill in a plugin structure:** Navigate to `skills/{name}/` subdirectory. Analyze only the skill directory, not plugin.json or sibling skills.
- **Skill that deliberately breaks conventions:** Note the deviation in the report. If the deviation is intentional and documented (e.g., a skill-about-skills that references its own pattern), flag but don't auto-penalize.
- **Empty skill directory:** Report as BLOCKED with "SKILL.md not found" as sole issue.
- **Skill with side effects (deploy, commit):** Note `disable-model-invocation` field presence/absence as a security check.

## Example: Good vs Bad X-Ray

**Bad X-Ray report:**
```
Score: 7/10. The skill is mostly good. Some improvements needed. [EXPLICIT]
Recommendation: Make it better. [EXPLICIT]
```
Failure: no evidence, no specific issues, no actionable fixes. [EXPLICIT]

**Good X-Ray report:**
```
Score: 7.2/10. Gate: CONDITIONAL (12/13 — fails checkpoint 6: no Good vs Bad example). [EXPLICIT]
Top issues:
1. [BLOCKER] No Good vs Bad example — affects calibration. Fix: Add concrete comparison in new section. [EXPLICIT]
2. [WARNING] Description lacks pushy context — affects triggering. Fix: Add "even if they don't explicitly ask" clause. [EXPLICIT]
3. [WARNING] references/patterns.md exists but SKILL.md never mentions it — affects progressive disclosure. [EXPLICIT]
```
Success: every finding is specific, evidenced, actionable, and tagged by severity. [EXPLICIT]

## Validation Gate

Before delivering the X-Ray report:

- [ ] Every file in the skill directory was read (not just SKILL.md)
- [ ] All 10 rubric dimensions have a numeric score with evidence cited
- [ ] All 13 gate checkpoints have a binary pass/fail with verification method
- [ ] Top 5 issues are prioritized: BLOCKERs before WARNINGs before INFOs
- [ ] Each issue has a specific action (not "improve" or "fix")
- [ ] Certification level matches the scoring formula: all dims >= 7, avg >= 8, gate 13/13
- [ ] Report follows the template structure (no missing sections, no extra commentary)

## Reference Files

| File | Content | Load When |
|------|---------|-----------|
| `references/gold-standard-anatomy.md` | What a 10/10 skill looks like: directory structure, frontmatter contract, body sections, progressive disclosure, writing rules, systemic requirements, evals schema | Always — needed for structural comparison |
| `references/quality-rubric.md` | 10-criterion rubric with 4-level scoring guides + detection methods, 13-point gate with verification commands, certification formula | Always — needed for scoring |

---
**Author:** Javier Montano | **Last updated:** March 18, 2026
