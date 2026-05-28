---
name: trigger-skill
description: 
  This skill should be used when the user asks to "optimize skill triggers",
  "improve skill description", "why isn't my skill triggering",
  "fix skill activation", "tune skill detection", or "make my skill
  fire correctly". Analyzes and optimizes a skill's frontmatter description
  for triggering accuracy — generating test queries, measuring trigger
  rates, iterating on the description, and producing the optimal version
  that maximizes true positives while minimizing false triggers. Use this
  skill whenever a skill under-triggers, over-triggers, or the user wants
  to ensure their description is production-grade. [EXPLICIT]
argument-hint: "path-to-skill-directory [--queries custom-queries.json]"
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

# Skill Trigger Optimizer

Optimize the single most important line in any skill: the frontmatter description. A perfect skill with a bad description never fires. A mediocre skill with a great description fires reliably and improves over time. [EXPLICIT]

This skill treats trigger optimization as a measurement problem, not a writing exercise. Generate test queries, measure accuracy, iterate, measure again. [EXPLICIT]

## Why This Exists

The description field is the primary mechanism Claude uses to decide which skill to invoke. Yet most skills are written description-first and never tested for triggering accuracy. The result: skills that under-trigger (user says the right thing, skill doesn't fire) or over-trigger (skill fires on unrelated requests). [EXPLICIT]

The Anthropic skill-creator has `improve_description.py` and `run_loop.py` for this purpose. This skill provides the same capability as a standalone tool, without requiring the full skill-creator plugin. [EXPLICIT]

## Usage

```
/trigger-skill /path/to/skill                           # auto-generate test queries
/trigger-skill /path/to/skill --queries my-queries.json  # use custom test queries
```

## The Optimization Process

### Step 1: Understand the Skill

Read SKILL.md completely. Extract: [EXPLICIT]
- **Current description** (the text to optimize)
- **Skill purpose** (what it actually does — from the body, not just the description)
- **Adjacent skills** (what it should NOT trigger on — skills with similar but different purposes)

Build a mental model: "This skill should fire when X, Y, Z. It should NOT fire when A, B, C." [EXPLICIT]

### Step 2: Generate Test Queries

Create 15-20 test queries split into two categories: [EXPLICIT]

**Should-Trigger (10-12 queries):**
- 3-4 exact match: phrases that are clearly this skill's domain ("audit my skill quality")
- 3-4 paraphrase: same intent, different words ("check if this skill is good enough")
- 2-3 implicit: user doesn't name the skill but the intent matches ("I made a skill, what do I do next?")
- 1-2 edge: borderline cases where triggering is debatable but probably correct ("review this SKILL.md")

**Should-NOT-Trigger (5-8 queries):**
- 2-3 adjacent domain: similar topic but different skill ("create a new skill from scratch" → skill-creator, not x-ray-skill)
- 2-3 unrelated: clearly different domain ("write a Python function to sort a list")
- 1-2 adversarial: contains trigger keywords but wrong context ("the word 'audit' in my essay about financial auditing")

**Output format:**
```json
{
  "skill_name": "x-ray-skill",
  "queries": [
    {"query": "audit my skill", "should_trigger": true, "category": "exact"},
    {"query": "is this Python code good?", "should_trigger": false, "category": "adjacent"}
  ]
}
```

### Step 3: Analyze Current Description

Score the current description against the test queries: [EXPLICIT]

| Query | Should Trigger? | Would Trigger? | Result |
|-------|----------------|---------------|--------|
| "audit my skill" | Yes | Yes | TRUE POSITIVE |
| "create a new skill" | No | Yes | FALSE POSITIVE |
| "is this skill ready to ship" | Yes | No | FALSE NEGATIVE |

Calculate metrics: [EXPLICIT]
- **True Positive Rate (TPR):** queries that should trigger and would / total should-trigger
- **False Positive Rate (FPR):** queries that shouldn't trigger but would / total should-not-trigger
- **Trigger Accuracy:** (true positives + true negatives) / total queries

**Baseline target:** TPR >= 80%, FPR <= 10%, Accuracy >= 85%.

### Step 4: Iterate on Description

For each false negative (should trigger but doesn't): [EXPLICIT]
- Identify what phrase or concept is missing from the description
- Add a trigger phrase or broader context clause

For each false positive (shouldn't trigger but does): [EXPLICIT]
- Identify what's too broad in the description
- Narrow with a scope qualifier or "NOT for" clause in the description

**Iteration protocol:**
1. Make one change to the description
2. Re-score against all test queries
3. If accuracy improved, keep the change. If degraded, revert. [EXPLICIT]
4. Repeat up to 3 iterations (diminishing returns beyond that)

**Constraint:** Description must remain under 1024 chars. Each iteration that adds text must also tighten elsewhere.

### Step 5: Validate Constraints

After optimization, verify the description still passes frontmatter rules: [EXPLICIT]
- [ ] Under 1024 characters
- [ ] Third person ("This skill should be used when...")
- [ ] 3-5 trigger phrases in quotes
- [ ] Pushy broader context ("even if they don't explicitly ask...")
- [ ] No angle brackets
- [ ] Accurately describes what the skill does (not just what triggers it)

**Trade-off: accuracy vs honesty.** A description that triggers perfectly but misrepresents the skill's capabilities is worse than an honest description with lower trigger accuracy. Optimize for trigger accuracy within the bounds of truthful description.

### Step 6: Produce Report

```markdown
# Trigger Optimization Report: {skill-name}

## Metrics
| Metric | Before | After | Delta |
|--------|--------|-------|-------|
| True Positive Rate | {%} | {%} | +{%} |
| False Positive Rate | {%} | {%} | -{%} |
| Trigger Accuracy | {%} | {%} | +{%} |

## Description
### Before
```
{original description}
```

### After
```
{optimized description}
```

### Changes Made
{numbered list of specific changes with reasoning}

## Test Query Results
| # | Query | Should | Before | After |
|---|-------|--------|--------|-------|
{full results table}

## Recommendation
{Apply the new description / Keep the original / Manual review needed}
```

## How Trigger Matching Works

Claude decides which skill to invoke by comparing the user's input against all available skill descriptions. Understanding the matching helps write better descriptions: [EXPLICIT]

| Factor | Impact | Implication for Description |
|--------|--------|---------------------------|
| Exact phrase match | Highest | Include 3-5 phrases users actually say, in quotes |
| Semantic similarity | High | Use synonyms and paraphrases for the same concept |
| Domain keywords | Medium | Include domain terms ("quality", "audit", "production") |
| Negation/scope | Low | "NOT for X" has weak negative signal — better to be specific about what it IS |
| Description length | Diminishing | Beyond ~300 chars, additional text has less marginal trigger value |

**The pushy principle:** Claude tends to under-trigger skills. Descriptions should slightly over-claim scope ("even if they don't explicitly ask for...") rather than under-claim. A user who gets an unexpected but relevant skill invocation is pleasantly surprised; a user whose skill never fires is frustrated.

## Assumptions & Limits

- Cannot run live triggering tests — analysis is based on semantic matching against the description text, not actual Claude routing behavior. Live testing requires the skill-creator's `run_eval.py`.
- Optimizing for one skill's triggers may affect adjacent skills' trigger rates. If two skills have similar descriptions, improving one may degrade the other. Note adjacency conflicts in the report.
- 3 iteration maximum balances improvement against context cost. Beyond 3, changes tend to oscillate rather than converge.
- The 1024-char description limit is a hard constraint. Optimization must fit within it.
- Trigger matching is probabilistic, not deterministic. The same query may trigger differently across sessions. Optimize for high probability, not guaranteed triggering.

### Failure Modes

| Failure | Signal | Recovery |
|---------|--------|----------|
| All queries show as "would trigger" | Description is too broad | Focus iteration on narrowing: add scope boundaries, remove vague phrases |
| Few queries trigger | Description is too narrow | Add trigger phrases, broader context, synonym coverage |
| Accuracy oscillates across iterations | Conflicting requirements (broad enough to trigger, narrow enough to not false-positive) | Accept the best iteration and note the conflict in the report |
| Description exceeds 1024 chars | Optimization added too much | Tighten: remove the lowest-value phrase, merge overlapping triggers |
| Adjacent skill conflict | Improving this skill's triggers degrades a sibling | Report the conflict. Suggest differentiating the two descriptions. |

## Edge Cases

- **Skill with no description:** Generate one from the body content. This is creation, not optimization — note the baseline as 0%.
- **Skill that should trigger on everything:** Some skills (e.g., input-analyst as a pre-processor) have intentionally broad triggers. Optimize for minimal false positives rather than high true positives.
- **Skill in a plugin with many siblings:** Adjacency conflicts are more likely. Include 2-3 sibling skill descriptions in the analysis to avoid cross-triggering.
- **User provides custom test queries:** Use them directly (skip Step 2). Still validate they have both should-trigger and should-not-trigger categories.
- **Description already at 1024 chars:** No room to add. Optimization must replace, not append. Focus on swapping low-value phrases for high-value ones.

## Example: Good vs Bad Optimization

**Bad:**
```
Before: "Analyzes skills for quality." [EXPLICIT]
After: "Analyzes skills for quality and production readiness." [EXPLICIT]
Change: Added "and production readiness." [EXPLICIT]
```
No test queries. No metrics. No evidence the change improved anything. [EXPLICIT]

**Good:**
```
Before: "Analyzes skills for quality." — TPR 40%, FPR 20%, Accuracy 55% [EXPLICIT]
After: "This skill should be used when the user asks to 'audit a skill', [EXPLICIT]
'review skill quality', or 'is this skill ready'. Reads a skill directory
and scores against gold standard." — TPR 83%, FPR 5%, Accuracy 90%
Changes: (1) Added third person framing. (2) Added 3 trigger phrases from [EXPLICIT]
test queries that were false negatives. (3) Added functional description
to reduce false positives from vague "quality" keyword. [EXPLICIT]
```

## Validation Gate

Before delivering the trigger optimization report: [EXPLICIT]

- [ ] 15-20 test queries generated with both should-trigger and should-not categories
- [ ] Metrics calculated for both before and after states
- [ ] Description remains under 1024 chars after optimization
- [ ] Description passes all frontmatter validation rules
- [ ] Each change has a reasoning traced to a specific test query result
- [ ] Adjacent skill conflicts (if any) are identified and reported

## Reference Files

| File | Content | Load When |
|------|---------|-----------|
| `references/trigger-patterns.md` | Common trigger failures by type, phrase templates for different skill categories, adjacency conflict resolution strategies | Always — needed for query generation and iteration guidance |

---
**Author:** Javier Montano | **Last updated:** March 18, 2026
