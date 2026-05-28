---
name: benchmark-skill
description: 
  This skill should be used when the user asks to "compare skill versions",
  "benchmark this skill", "what improved", "diff these skills",
  "measure skill improvement", or "before and after analysis". Compares
  two states of a skill — different versions, before/after improvement,
  or one skill against another — and produces a dimension-by-dimension
  delta report with quantified improvement. Use this skill whenever
  someone needs proof that an improvement actually improved something,
  or to compare a skill against a reference standard. [EXPLICIT]
argument-hint: "path-a path-b | path --against-standard"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
model: opus
context: fork
version: 1.0.0
---

# Skill Benchmark

Quantified comparison between two skill states. Measures improvement dimension by dimension, identifies regressions, and produces evidence that changes actually made things better — or exposes that they didn't. [EXPLICIT]

Without measurement, improvement is anecdotal. This skill turns "I think it's better" into "Clarity improved from 6 to 9, but density dropped from 8 to 7 due to added filler in section X." [EXPLICIT]

## Usage

```
/benchmark-skill /path/to/skill-v1 /path/to/skill-v2      # compare two directories
/benchmark-skill /path/to/skill --against-standard          # compare against gold standard
```

### Input Modes

| Mode | Input | Output | Use When |
|------|-------|--------|----------|
| **Version comparison** | Two skill directory paths | Delta report: dimension-by-dimension + net assessment | Measuring improvement after surgeon-skill or manual edits |
| **Standard comparison** | One skill path + `--against-standard` | Gap-to-standard report: how far from 10/10 | Evaluating a skill's absolute quality without a prior version |

## The Benchmark Process

### Step 1: Inventory Both States

For each skill state (A and B, or skill and standard): [EXPLICIT]

| Attribute | State A | State B | Delta |
|-----------|---------|---------|-------|
| Total files | | | +N/-N |
| Total lines | | | +N/-N |
| SKILL.md lines | | | +N/-N |
| Reference files | | | +N/-N |
| Evals count | | | +N/-N |
| Has agents/ | | | |
| Has scripts/ | | | |

### Step 2: Score Both States

Apply the 10-criterion rubric from x-ray-skill's `references/quality-rubric.md` to both states independently. Produce parallel scorecards. [EXPLICIT]

**Scoring consistency:** Use the same evidence standards for both states. If you give State A a 7 on clarity because of 2 ambiguous pronouns, State B with 1 ambiguous pronoun should score higher — don't use different scales.

| # | Criterion | State A | State B | Delta | Direction |
|---|-----------|---------|---------|-------|-----------|
| 1 | Foundation | /10 | /10 | | Better/Worse/Same |
| 2 | Truthfulness | /10 | /10 | | |
| 3 | Quality | /10 | /10 | | |
| 4 | Density | /10 | /10 | | |
| 5 | Simplicity | /10 | /10 | | |
| 6 | Clarity | /10 | /10 | | |
| 7 | Precision | /10 | /10 | | |
| 8 | Depth | /10 | /10 | | |
| 9 | Coherence | /10 | /10 | | |
| 10 | Value | /10 | /10 | | |
| | **Average** | **/10** | **/10** | | |

### Step 3: Run Gate on Both States

Apply the 13-point meta-validation gate to both: [EXPLICIT]

| # | Checkpoint | State A | State B | Changed? |
|---|-----------|---------|---------|----------|
| 1-13 | ... | PASS/FAIL | PASS/FAIL | Fixed/Regressed/Same |

### Step 4: Identify Regressions

A regression is any dimension where State B scores lower than State A, or any gate checkpoint that passed in A but fails in B. [EXPLICIT]

**Regressions are the most important finding.** Improvements are expected (that's the point of making changes). Regressions are unexpected — they indicate unintended consequences.

For each regression: [EXPLICIT]
- **Which dimension or checkpoint regressed**
- **What specific change caused the regression** (trace to a file diff)
- **How severe** (1-point drop vs 3-point drop)
- **Whether the regression is a trade-off** (e.g., adding content improved depth but reduced density)

### Step 5: Identify Key Improvements

For each dimension that improved by 2+ points: [EXPLICIT]
- **What specific change drove the improvement** (trace to file/section)
- **Whether the improvement is genuine or inflationary** (adding a "Good vs Bad" section earns the points; adding filler does not)

### Step 6: Net Assessment

```
IMPROVED:    More dimensions improved than regressed, average increased, no gate regressions [EXPLICIT]
LATERAL:     Similar average, trade-offs balance (gained depth, lost density) [EXPLICIT]
REGRESSED:   More dimensions regressed than improved, or gate regressions [EXPLICIT]
TRANSFORMED: Fundamental structural change — scores aren't directly comparable (e.g., single-file → multi-file) [EXPLICIT]
```

### Step 7: Produce Benchmark Report

```markdown
# Benchmark Report: {skill-name}

**Compared:** {State A description} vs {State B description}
**Net Assessment:** {IMPROVED / LATERAL / REGRESSED / TRANSFORMED}

## Summary
| Metric | State A | State B | Delta |
|--------|---------|---------|-------|
| Average score | /10 | /10 | +N |
| Gate pass | /13 | /13 | +N |
| Dimensions improved | | {count} | |
| Dimensions regressed | | {count} | |
| Dimensions unchanged | | {count} | |

## Dimension-by-Dimension
| # | Criterion | A | B | Delta | Key Driver |
|---|-----------|---|---|-------|-----------|
| 1-10 | ... | /10 | /10 | +/-N | {what caused the change} |

## Gate Changes
| # | Checkpoint | A | B | Change |
|---|-----------|---|---|--------|
{only rows that changed}

## Regressions (if any)
| Dimension | A→B | Cause | Severity | Trade-off? |
|-----------|-----|-------|----------|-----------|
{each regression with root cause analysis}

## Top Improvements
| Dimension | A→B | Driver | Genuine? |
|-----------|-----|--------|----------|
{improvements of 2+ points}

## Recommendation
{specific next action based on the assessment}
```

## Assumptions & Limits

- Read-only. This skill reads both states but never modifies either.
- Scoring both states in the same session ensures consistent scale. Comparing scores from different sessions (e.g., an old x-ray-skill report vs a new one) may have 1-point variance on subjective dimensions.
- "Against standard" mode compares against the theoretical 10/10, not against a specific real skill. The gold standard is the reference anatomy and rubric, not the skill-creator itself.
- Cannot measure runtime behavior improvement. A skill that scores better structurally may still produce worse output if instruction logic changed. Use evals for behavioral comparison.
- For version comparison, both paths must contain SKILL.md. If State A was deleted, use a git checkout to restore it, or provide the .skill ZIP of the earlier version.

### Failure Modes

| Failure | Signal | Recovery |
|---------|--------|----------|
| States are identical | All deltas are zero | Report: "No changes detected between states." Verify paths are correct. |
| State A doesn't exist | Path invalid or SKILL.md missing | Ask user for correct path. Suggest `git log` to find prior versions. |
| Incomparable states | Fundamental restructure (single-file → 10-file) | Report as TRANSFORMED. Score both independently. Note that direct delta comparison is misleading for structural overhauls. |
| Score inconsistency | Same unchanged section gets different scores in A vs B | Re-score the unchanged section using State A's evidence. Consistency requires anchoring to the first assessment. |

## Edge Cases

- **Comparing against gold standard:** State A = the skill, State B = theoretical 10/10 on all dimensions. Delta shows the gap to perfect. Regressions are impossible (can't regress below yourself).
- **Comparing the same skill at two git commits:** Extract both versions to temp directories. Note the commits in the report header.
- **One-file → multi-file transformation:** TRANSFORMED assessment. Coherence dimension goes from N/A (single-file) to scored (multi-file). This appears as a new dimension, not an improvement from 0.
- **User compares two different skills (not versions):** Valid use case — "which of these two skills is better?" Report both scorecards side by side. Net assessment: which skill is stronger overall and on which dimensions.
- **Benchmark after trigger-skill optimization:** Only the description changed. Most dimensions should be unchanged. Trigger accuracy metrics (if available) are the primary comparison point.

## Example: Good vs Bad Benchmark

**Bad:**
```
State A: 7.2/10. State B: 8.1/10. Improvement: +0.9. Good job. [EXPLICIT]
```
No dimension breakdown. No regression detection. No evidence. [EXPLICIT]

**Good:**
```
Net: IMPROVED (+0.9 average, 0 regressions, 3 gate fixes) [EXPLICIT]
Key improvements: Depth 5→8 (added failure modes + 4 edge cases), [EXPLICIT]
                  Clarity 6→9 (added glossary, eliminated ambiguous pronouns). [EXPLICIT]
Key trade-off: Density 9→8 (added content increased value but reduced compression). [EXPLICIT]
Regressions: None. [EXPLICIT]
Gate: 10/13 → 13/13 (fixed: Good vs Bad example, 2 missing edge cases). [EXPLICIT]
```

## Validation Gate

Before delivering the benchmark report: [EXPLICIT]

- [ ] Both states were scored with consistent criteria (same rubric, same evidence standards)
- [ ] Every dimension has a score for both states with key driver identified
- [ ] All regressions are identified with root cause and severity
- [ ] Net assessment matches the data (not assigned by feel)
- [ ] "Against standard" mode correctly uses theoretical 10/10, not a real skill
- [ ] Report follows the template structure

## Reference Files

| File | Content | Load When |
|------|---------|-----------|
| `references/comparison-framework.md` | Scoring consistency protocols, delta classification rules, trade-off analysis framework, TRANSFORMED assessment criteria | Always — needed for rigorous comparison |

---
**Author:** Javier Montano | **Last updated:** March 18, 2026
