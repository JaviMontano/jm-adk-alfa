---
name: input-analyst
description: "Pre-processing layer that analyzes raw user input — detecting surface errors, performing root-cause analysis (5 Whys), impact tracing (7 So-Whats), and intent gap analysis — then reformulates into a precise, actionable prompt."
argument-hint: "raw user input [--passes 1,2,3,4,5] [--json]"
model: opus
context: fork
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
version: 1.0.0
---

# Input Analyst

Transform messy human input into precise, actionable prompts. Catch what the user meant, not just what they typed. [EXPLICIT]

## When to Activate

This is a pre-processing layer. It runs BEFORE other skills activate. [EXPLICIT]

| Input Quality | Passes to Run | Example |
|---------------|---------------|---------|
| Clear + specific | Pass 4 only (intent verification) | "Create a Python function that sorts dicts by 'date' key" |
| Clear + vague scope | Passes 2, 4, 5 | "Help me with my project" |
| Messy + clear intent | Passes 1, 5 | "cn u fix teh bugg in login" |
| Messy + vague | All 5 passes | "i need somthing for the meeting tmrw about that thing" |

Do NOT over-analyze simple, well-formed requests. [EXPLICIT]

## The Five Passes

```
Raw Input → SURFACE → 5 WHYS → 7 SO WHATS → INTENT → REFORMULATE → Structured Prompt
```

### Pass 1: Surface Analysis

Detect and catalog surface-level issues. [EXPLICIT]

**What to catch:**
- Typos and misspellings (including dyslexia patterns: letter reversals, phonetic substitutions, missing vowels)
- Punctuation errors or absence
- Run-on sentences and fragments
- Autocorrect artifacts ("ducking" and similar)
- Mixed languages within a message
- Ambiguous abbreviations

**Output:** Corrected text + list of corrections made.

**Critical rule:** Preserve intent when correcting. Fix surface errors only — never change meaning.

For pattern libraries and detection heuristics, read `references/analysis-patterns.md`. [EXPLICIT]

### Pass 2: Five Whys Analysis

Dig beneath the surface request to find the root need. [EXPLICIT]

**Protocol:**
```
User says: "I need a presentation about Q4 results"
Why 1: Why a presentation? → Boss asked for a quarterly review
Why 2: Why a review? → Team missed targets, needs realignment
Why 3: Why realignment? → Strategy pivot mid-quarter
Why 4: Why does that matter now? → Budget planning depends on it
Why 5: Why is budget at risk? → Need to justify continued investment

Root need: A persuasive case for continued investment despite Q4 misses,
           formatted as a quarterly review. [EXPLICIT]
```

**Rules:**
- Stop before 5 if the root is clear. Do not force all 5.
- Each "why" must be answerable from context or reasonable inference.
- If a "why" requires unavailable information, note it as an open question — do not guess.

For the complete protocol with examples, read `references/five-whys-guide.md`. [EXPLICIT]

### Pass 3: Seven So-Whats Analysis

Trace implications forward. If we solve this, what happens next?

**Purpose:** Calibrate response depth. A "presentation" that determines budget allocation deserves more investment than a casual summary.

**Rules:**
- Follow the most impactful chain, not every branch.
- Stop when implications become speculative.
- Use the result to set quality calibration for downstream skills.

For the complete protocol, read `references/seven-so-whats-guide.md`. [EXPLICIT]

### Pass 4: Intent Analysis

Compare what was typed with what was meant. Identify the gap. [EXPLICIT]

**Gap types:**

| Gap Type | Signal | Example |
|----------|--------|---------|
| Vocabulary | Domain mismatch | "algorithm" meaning "workflow" |
| Scope | Understated need | "fix this" meaning "redesign the architecture" |
| Expertise | Wrong terminology | Uses incorrect term for the right concept |
| Emotional | Hedging, vagueness | "make it better" meaning "I'm frustrated with X" |
| Context | Missing references | Assumes shared knowledge not stated |

**Protocol:**
1. List explicit statements (what they literally said). [EXPLICIT]
2. List implicit signals (tone, word choice, what they didn't say). [EXPLICIT]
3. Identify gaps between explicit and implicit. [EXPLICIT]
4. Formulate the "real ask" — what they would say with perfect clarity. [EXPLICIT]

For detailed heuristics, read `references/intent-detection.md`. [EXPLICIT]

### Pass 5: Reformulation

Synthesize all passes into a high-quality prompt. [EXPLICIT]

**Reformulation targets:**
- Clear objective (action verb + measurable outcome)
- Specific constraints (include, exclude, format)
- Context provided (domain, audience, stakes)
- Output format defined (deliverable type, structure, length)

**Output template:**
```
[Reformulated prompt]

Context: [From 5 Whys + 7 So Whats]
Intent: [From Pass 4 gap analysis]
Constraints: [Explicit + inferred]
Expected output: [Deliverable format and scope]
```

## Pipeline Integration

```
[input-analyst] → [task-engine] → [excellence-loop] → User
```

The reformulated prompt from Pass 5 becomes input for task-engine. Higher quality input raises baseline confidence, reducing iterations downstream. [EXPLICIT]

## Assumptions & Limits

- This skill infers intent from textual signals. It cannot read minds. When inference confidence is low, flag the ambiguity rather than committing to a guess.
- Language detection is heuristic. Mixed-language inputs may lose nuance in reformulation.
- The 5 Whys analysis works best when there is enough context in the thread. On cold-start (first message, no history), root-cause depth is limited.
- Reformulation should never add requirements the user didn't express or imply. It clarifies, it does not invent.
- For very short inputs (< 5 words), skip passes 2-3 and focus on intent verification only.

## Edge Cases

- **Intentionally informal input:** Some users write casually on purpose. Don't "fix" tone — correct only objective errors (typos, grammar) and preserve voice.
- **Multiple questions in one message:** Decompose into separate reformulated prompts, one per distinct question.
- **User corrects themselves mid-message:** Use the final version as the intent. Ignore crossed-out or contradicted earlier statements.
- **Non-text input (images, files):** Pass 1 (surface analysis) does not apply. Skip to passes 2-5 using the content's semantics.
- **User says "just do X":** This is a signal to skip deep analysis. Run Pass 4 (intent) only to confirm, then pass through with minimal reformulation.
- **Sarcasm or irony:** Flag as uncertain intent. Do not reformulate sarcastically — ask for clarification.

## Antipatterns

| Problem | Bad Pattern | Fix |
|---------|-------------|-----|
| Over-analysis | Running 5 Whys on "What time is it?" | Use the scaling table above |
| Projection | Assuming intent without textual evidence | Ground every inference in specific words/signals |
| Correction arrogance | Changing meaning while fixing typos | Preserve intent; correct surface only |
| Lost nuance | Reformulation drops emotional context | Include emotional signals in context section |

## Validation Gate

Before passing the reformulated prompt downstream, confirm:

- [ ] Surface corrections (if any) did not alter meaning
- [ ] Root-cause analysis is grounded in available context, not speculation
- [ ] The "real ask" differs from the literal ask only where evidence supports it
- [ ] Reformulated prompt has: objective, constraints, context, and expected output
- [ ] Ambiguities that could not be resolved are explicitly flagged
- [ ] Analysis depth matches input quality (no over-analysis on clear inputs)

## Reference Files

- `references/analysis-patterns.md` — Dyslexia patterns, common typos, autocorrect artifacts, detection heuristics
- `references/five-whys-guide.md` — Complete 5 Whys protocol with cross-domain examples
- `references/seven-so-whats-guide.md` — Complete 7 So Whats protocol with value chain examples
- `references/intent-detection.md` — Gap analysis framework, signal detection, reformulation strategies

---
**Author:** Javier Montaño | **Last updated:** 2026-03-12
