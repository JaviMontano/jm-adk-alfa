# Certification Checklist

Complete checklist for certify-skill. Organized by phase. Each check has a verification method and pass criteria so certification is reproducible.

## Phase 1: Structural Validation (automated, deterministic)

No judgment required. Run commands, record results.

| # | Check | Command | Pass Criteria | Severity if Fail |
|---|-------|---------|---------------|-----------------|
| S1 | SKILL.md at skill root | `ls {path}/SKILL.md` | File exists | BLOCKER — abort all phases |
| S2 | Under 500 lines | `wc -l {path}/SKILL.md` | <= 500 | WARNING — content may need extraction to references/ |
| S3 | name is kebab-case | Parse frontmatter; `^[a-z0-9]+(-[a-z0-9]+)*$` | Match, <= 64 chars | BLOCKER — skill can't route |
| S4 | description under 1024 chars | Parse frontmatter; count chars | <= 1024 | WARNING — may be truncated |
| S5 | No angle brackets in description | Check for `<` or `>` in description | None found | BLOCKER — breaks YAML parsing |
| S6 | All referenced files exist | Grep file paths in SKILL.md → `ls` each | All resolve | BLOCKER — broken progressive disclosure |
| S7 | No orphan files | `ls -R` all files → check each appears in SKILL.md | Zero orphans | WARNING — wasted context/space |
| S8 | evals.json valid (if exists) | `python3 -m json.tool {path}/evals/evals.json` | Valid JSON | WARNING — eval loop won't work |
| S9 | No old path patterns | `grep -r 'reference/\|tools/' {path}` | Zero matches for singular `reference/` or old `tools/` paths; plural `references/` is valid | WARNING — stale references from rename |

**Phase 1 abort rule:** If S1 fails, report BLOCKED with the single issue "SKILL.md not found at {path}" and skip all remaining phases. Everything depends on SKILL.md existing.

## Phase 2: Content Validation (judgment required)

Read the skill and evaluate. Each check requires reading content, not just running commands.

### 2A. Frontmatter Quality

| # | Check | Criteria | Pass | Fail Example |
|---|-------|---------|------|-------------|
| F1 | Third person | Description starts with "This skill should be used when..." or equivalent third-person framing | "This skill..." | "I analyze..." |
| F2 | 3-5 trigger phrases | Description contains 3-5 quoted phrases users would actually say | 4 specific phrases | Generic "for data analysis" |
| F3 | Pushy context | Includes broader trigger logic ("even if they don't explicitly ask...") | Broader context present | Description stops at literal triggers |
| F4 | Minimal allowed-tools | Only tools the skill actually calls; no over-permissioning | Read+Grep for read-only skill | All 7 tools listed for a read-only skill |

### 2B. Body Sections

| # | Section | Required? | Pass Criteria | What "Substantive" Means |
|---|---------|-----------|---------------|-------------------------|
| B1 | Title + value prop | Yes | 1-2 sentences answering "why does this exist?" | Not just a name restatement |
| B2 | Usage / When to Activate | Yes | 2+ invocation examples with arguments shown | Not just "use this skill when needed" |
| B3 | Before {Action} | Recommended | Each reference file has a load condition AND skip condition | Not just listing files without conditions |
| B4 | Core Process | Yes | Actionable instructions; tables for structured data; code blocks for templates | Not just prose describing the concept |
| B5 | Assumptions & Limits | Yes | 3+ specific limits, each with what happens when hit | Not "may have limitations" |
| B6 | Edge Cases | Yes, 3+ | Each has: scenario + detection + handling instruction | Not just listing scenarios without handling |
| B7 | Good vs Bad Example | Yes, 1+ | Side-by-side comparison with reasoning for the difference | Not just "do this, not that" without why |
| B8 | Validation Gate | Yes, 5+ | Testable checkboxes; each can be verified by a reader | Not "ensure quality" (untestable) |
| B9 | Reference Files | When refs exist | Table with: file path + content summary + load-when condition | Not a bare file list |

### 2C. Writing Quality

| # | Check | Detection Method | Pass Threshold |
|---|-------|-----------------|---------------|
| W1 | Imperative form | `grep -c 'you should\|you can\|you need to' SKILL.md` | 0 occurrences |
| W2 | No CAPS emphasis | Grep ALL CAPS words excluding acronyms (API, JSON, YAML, etc.) | 0 occurrences |
| W3 | Tables for structured data | Count tables vs bullet lists for data with 2+ dimensions | Tables >= bullets |
| W4 | Code blocks for templates | All output format specifications shown in code blocks | 100% in blocks |
| W5 | One concern per section | No section covers 2+ unrelated topics | Zero multi-topic sections |

## Phase 3: Systemic Coherence (multi-file only)

Skip for single-file skills — report all as N/A.

| # | Check | Method | Pass Criteria | Common Violation |
|---|-------|--------|---------------|-----------------|
| C1 | Unified terminology | Pick 5 key terms → grep across all files | Same concept = same word everywhere | "root need" in SKILL.md, "root cause" in references |
| C2 | No duplication | Spot-check 3 paragraphs from references against SKILL.md | No verbatim matches beyond 1-sentence pointers | Entire section copied into both SKILL.md and a reference |
| C3 | Evidence taxonomy | Check claim-tagging system across files | One system everywhere | SKILL.md uses explicit/inferred/open, references use quantified/qualified |
| C4 | Schema alignment | Compare output template fields in SKILL.md to JSON in workflow/evals | Field names match 1:1 | SKILL.md says "goal", JSON says "objective" |
| C5 | Lean integration | Reference files' pipeline sections | 3-5 lines pointing to SKILL.md | Full re-explanation of the pipeline in the reference |

## Phase 4: Quality Rubric (10 dimensions)

Score each 1-10. When x-ray-skill's `references/quality-rubric.md` is available, use its detailed 4-level scoring guides and detection methods. When running standalone, use these summaries:

| # | Criterion | 10 Means | 7 Means | Detection |
|---|-----------|----------|---------|-----------|
| 1 | Foundation | Every rule has reasoning. Trade-offs cited. | Most grounded. 2-3 rules without why. | Count ungrounded rules / total rules |
| 2 | Truthfulness | Every claim verifiable or marked estimate. | 1-2 soft claims. | Grep for %, time estimates, superlatives |
| 3 | Quality | Consistent formatting. All refs resolve. | Minor inconsistencies. | Check headings, refs, tables |
| 4 | Density | Every sentence unique. Zero cross-file duplication. | Occasional redundancy. | Delete-test per paragraph |
| 5 | Simplicity | Fewest words preserving precision. | A few over-explained concepts. | Word count per concept |
| 6 | Clarity | Zero ambiguity. Terms defined. | A few dual-interpretation statements. | Grep for undefined pronouns |
| 7 | Precision | All thresholds numeric. All criteria testable. | A few vague qualifiers. | Grep for "appropriate", "reasonable" |
| 8 | Depth | 5+ edge cases. Failure modes. Trade-offs. | 3+ edge cases. Some failures. | Count edge cases, failures, trade-offs |
| 9 | Coherence | Same term = same word cross-file. | 1-2 variants. | Grep key terms across files |
| 10 | Value | Delete any section → degradation. | 1-2 nice-to-have sections. | Delete-test per section |

**Scoring requirement:** Each score needs a one-sentence justification with evidence. "Clarity: 8" is not a finding. "Clarity: 8 — all terms defined in Glossary, zero ambiguous pronouns" is a finding.

## Phase 5: MOAT Validation (extends CERTIFIED)

A skill that passes CERTIFIED must also pass these 5 checks to achieve MOAT status. All checks are deterministic.

| # | Check | Command | Pass Criteria | Severity if Fail |
|---|-------|---------|---------------|-----------------|
| M1 | evals/evals.json exists | `ls {path}/evals/evals.json` | File exists | BLOCKER — no automated quality assurance |
| M1b | >= 5 distinct evals | Parse evals.json, count entries | >= 5 entries with distinct `id` or `name` fields | BLOCKER — insufficient coverage |
| M2 | False-positive eval | Grep for `"false_positive"` or eval named `*false*` or `*negative*` | >= 1 match | WARNING — no guard against over-triggering |
| M2b | Edge-case eval | Grep for `"edge_case"` or eval named `*edge*` or `*boundary*` | >= 1 match | WARNING — no edge coverage |
| M3 | References substantive | For each file in references/: `wc -l` and `grep -c 'pending\|pending\|template'` | All files >= 20 lines AND zero pending/pending/template | BLOCKER — broken progressive disclosure |
| M4 | Template A compliance | Grep for required sections: "## Usage" or "## When to Activate", "## Validation Gate" or "## Quality Gate" | Both present | BLOCKER — skill doesn't follow current standard |
| M4b | No Template B markers | `grep -c '## The Physics\|## The Protocol\|## TL;DR' SKILL.md` | 0 matches | BLOCKER — deprecated template |
| M5 | Evidence tag coverage | Count `[EXPLICIT]\|[INFERRED]\|[OPEN]` occurrences / count factual sentences | >= 80% (for Standard/Orchestrator tiers); >= 50% (for Utility tier) | WARNING — ungrounded claims |

**Phase 5 skip rule:** If Phase 1-4 result in BLOCKED, skip Phase 5. MOAT requires passing CERTIFIED first.

## Certification Formula

```
MOAT:          CERTIFIED + all M1-M5 pass (zero BLOCKER failures in Phase 5)
CERTIFIED:     All dimensions >= 7/10 AND average >= 8.0/10 AND all S1-S9 pass
CONDITIONAL:   Average >= 8.0 BUT 1-2 dimensions at 6/10 OR 1-2 structural failures
BLOCKED:       Any dimension < 6/10 OR 3+ structural failures OR S1 fails
```

**Threshold edge cases:**
- Average exactly 8.0 with all dims >= 7: CERTIFIED
- Average 7.9 with all dims >= 7: CONDITIONAL (formula is strict on the average)
- One dim at 6, rest at 9+, average 8.5: CONDITIONAL (the 6 blocks full certification)
- Single-file skill with coherence N/A: average calculated from 9 dimensions, not 10

## Certification Report Template

```markdown
# Certification Report: {skill-name}

**Date:** {date}
**Certification:** {CERTIFIED / CONDITIONAL / BLOCKED}
**Overall Score:** {average}/10
**Structural:** {N}/9 pass
**Content:** {N}/18 pass
**Systemic:** {N}/5 pass (or N/A)

## Rubric Scores
| # | Criterion | Score | Evidence |
|---|-----------|-------|----------|
| 1 | Foundation | /10 | {one sentence citing specific finding} |
| 2 | Truthfulness | /10 | |
| 3 | Quality | /10 | |
| 4 | Density | /10 | |
| 5 | Simplicity | /10 | |
| 6 | Clarity | /10 | |
| 7 | Precision | /10 | |
| 8 | Depth | /10 | |
| 9 | Coherence | /10 | |
| 10 | Value | /10 | |
| | **Average** | **/10** | |

## Structural Checks (Phase 1)
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| S1-S9 | {description} | PASS/FAIL | {command output} |

## Content Checks (Phase 2)
| # | Check | Result |
|---|-------|--------|
| F1-F4 | {description} | PASS/FAIL |
| B1-B9 | {description} | PASS/FAIL |
| W1-W5 | {description} | PASS/FAIL |

## Systemic Checks (Phase 3)
| # | Check | Result |
|---|-------|--------|
| C1-C5 | {description} | PASS/FAIL/N/A |

## Blockers (CONDITIONAL or BLOCKED only)
| # | Issue | Fix Required | Estimated Effort |
|---|-------|-------------|-----------------|
| 1 | {specific finding} | {specific action} | {time estimate} |

## Delta from Prior Certification (if re-certifying)
| Dimension | Before | After | Change |
|-----------|--------|-------|--------|
| {name} | {score} | {score} | +N / -N / = |

## Recommendation
- CERTIFIED: "Ship it. This skill meets production quality standards."
- CONDITIONAL: "Fix {N} blockers listed above, then re-certify. Estimated total effort: {time}."
- BLOCKED: "Run `/surgeon-skill {path}` to address {N} foundational issues before re-certifying."
```

---
**Author:** Javier Montano | **Last updated:** March 18, 2026
