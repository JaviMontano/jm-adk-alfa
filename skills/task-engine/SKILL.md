---
name: task-engine
description: 
  Meta-cognitive reasoning engine that decomposes complex problems using the DSVSR protocol
  (Decompose-Solve-Verify-Synthesize-Reflect) with explicit confidence calibration. [EXPLICIT]
  Use when the user asks to "break down this problem", "analyze with confidence scores",
  "decompose and verify", "run DSVSR", or "reason through this step by step". [EXPLICIT]
argument-hint: "problem description [--target 0.95] [--fast]"
model: opus
context: fork
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Edit
  - Write
  - WebSearch
  - WebFetch
version: 1.0.0
---

# Task Engine

Decompose, solve with confidence, verify, synthesize, and reflect — until the answer earns its confidence score. [EXPLICIT]

## When to Activate

| Signal | Route |
|--------|-------|
| 2+ complexity indicators (multi-domain, high-stakes, ambiguous, 50+ words) | Full DSVSR |
| Simple factual or single-domain question | Fast path — answer directly with implicit confidence |
| User specifies confidence threshold | Full DSVSR with custom target |

## The DSVSR Protocol

```
Problem → DECOMPOSE → SOLVE → VERIFY → SYNTHESIZE → REFLECT → Answer + Metadata
                                                         ↑              │
                                                         └──── if < target ──┘
```

### 1. DECOMPOSE

Break the problem into independent, atomic sub-problems. [EXPLICIT]

1. Strip noise — identify the core question. [EXPLICIT]
2. List components needing separate answers. [EXPLICIT]
3. Map dependencies (which block others?). [EXPLICIT]
4. Order by dependency chain (foundations first). [EXPLICIT]
5. Tag each by domain (technical, strategic, creative, factual). [EXPLICIT]

Output format:
```
Sub-problems identified: [N]
├── SP-1: [description] (domain: [X], depends on: none)
├── SP-2: [description] (domain: [X], depends on: SP-1)
└── SP-3: [description] (domain: [X], depends on: none)
```

**Trade-off:** Over-decomposition creates unnecessary overhead; under-decomposition hides complexity. Target 3-7 sub-problems. If you have more than 7, group related ones.

### 2. SOLVE

Answer each sub-problem with explicit confidence scoring. [EXPLICIT]

| Score | Meaning | Evidence Required |
|-------|---------|-------------------|
| 0.95-1.0 | Certain | Verifiable facts, direct evidence, mathematical proof |
| 0.85-0.94 | High | Strong evidence, expert consensus |
| 0.70-0.84 | Moderate | Reasonable inference, partial evidence |
| 0.50-0.69 | Low | Educated guess, significant assumptions |
| Below 0.50 | Speculative | Flag as hypothesis |

Per sub-problem:
```
SP-1: [Answer]
Confidence: [0.XX]
Justification: [Why this confidence level]
Would increase to [0.XX] if: [What additional info would help]
```

**Rules:**
- Never inflate confidence. Underestimate if unsure.
- If confidence < 0.70 on a critical sub-problem, flag immediately.
- When a sub-problem requires specialized expertise, consider delegating (see Delegation below).

### 3. VERIFY

Cross-check every sub-answer against four dimensions:

- **LOGIC:** Is reasoning internally consistent? Does conclusion follow from premises?
- **FACTS:** Are factual claims verifiable? Have I confused opinion with fact?
- **COMPLETENESS:** Have I considered all relevant aspects? What am I NOT addressing?
- **BIAS:** Am I anchored on my first solution? Confirming what I already believe? Would someone with different expertise disagree?

**Bias signals to watch:** Anchoring (first answer feels "obviously right"), confirmation (only supporting evidence found), availability (overweighting recent examples), authority (accepting a framework because it's popular, not because it fits).

After verification, update confidence scores. If scores don't change, verification was superficial. [EXPLICIT]

### 4. SYNTHESIZE

Combine verified sub-answers into a coherent response. [EXPLICIT]

1. Start with highest-confidence sub-answers (foundation). [EXPLICIT]
2. Layer moderate-confidence answers with caveats. [EXPLICIT]
3. Resolve conflicts: identify source of tension between contradicting sub-answers. [EXPLICIT]
4. Mark clearly: **certainty** vs **hypothesis**. [EXPLICIT]
5. Compute global confidence: `Global = sum(sub_confidence * sub_importance) / sum(sub_importance)`. [EXPLICIT]

**Conflict resolution priority:** Verified facts > Logical deductions > Expert consensus > Reasonable inference > Flagged speculation.

### 5. REFLECT

If global confidence < target (default 0.95):

1. Identify the weakest sub-problem. [EXPLICIT]
2. Diagnose: data gap, logic gap, or expertise gap?
3. If retrievable — gather info and retry that sub-problem. [EXPLICIT]
4. If not retrievable — deliver with explicit uncertainty flagged. [EXPLICIT]
5. If fundamentally unknowable — state this clearly. [EXPLICIT]

**Reflection questions:** What is the single biggest weakness? If I'm wrong, what's the most likely cause? What would a disagreeing expert say? Is there a simpler explanation I'm overlooking?

## Information Recursion

Before producing any answer, scan:
1. **Thread context** — all previous messages
2. **Attachments** — all files and documents provided
3. **Stated preferences** — format, depth, style instructions
4. **Implicit context** — time constraints, audience, stakes

Always include a completeness statement:
```
Sources reviewed: [thread messages and attachments consulted]
Information gaps: [what was NOT available that would improve confidence]
```

## Fast Path

Skip DSVSR when the question has fewer than 2 complexity signals. Answer directly with clarity and relevant caveats. [EXPLICIT]

**Complexity signals:** Multi-domain, 50+ words, high ambiguity, high stakes, multiple dependencies.

## Agent Delegation

Route specialized sub-problems to domain experts:

| Domain | Route |
|--------|-------|
| Mathematical/statistical | math-reasoning subagent |
| Code analysis/debugging | code-analysis subagent |
| Data analysis | data-analysis subagent |
| General knowledge | handle inline |

Each delegate returns: answer + confidence + evidence. Task-engine aggregates. [EXPLICIT]

## Confidence Metadata Output

Every substantial response includes:

```
---
REASONING METADATA:
- Global confidence: [0.XX]
- Sub-problem confidence: [SP-1: 0.XX, SP-2: 0.XX, ...]
- Sources consulted: [thread messages, attachments, knowledge]
- Weaknesses identified: [if any]
- Rigidity level: [exploratory | analytical | executive]
- Verification status: [all checks passed | N flags raised]
```

**Rigidity levels:**
- **Exploratory** — multiple valid paths, presenting options
- **Analytical** — clear methodology applied, confident in process
- **Executive** — single recommendation, high confidence, ready to act

## Pipeline Integration

```
[input-analyst] → [task-engine] → [excellence-loop] → User
```

Higher input quality from input-analyst raises baseline confidence, reducing DSVSR iterations. [EXPLICIT]

## Assumptions & Limits

- Confidence scores are self-assessed, not externally validated. They indicate reasoning quality, not ground truth.
- The 0.95 default target is aggressive. For exploratory work, lower to 0.80.
- DSVSR adds latency. Do not run full protocol on simple questions — the fast path exists for a reason.
- Agent delegation assumes subagents are available. If not, handle inline with a confidence penalty note.
- Maximum 3 REFLECT retries to prevent infinite loops.

## Edge Cases

- **Circular dependencies in decomposition:** If SP-2 depends on SP-3 and SP-3 depends on SP-2, merge them into a single sub-problem or introduce an assumption to break the cycle.
- **All sub-problems below 0.50:** The problem is likely under-specified. Ask the user for clarification rather than guessing.
- **Conflicting sub-answers with equal confidence:** Escalate the conflict explicitly. Present both interpretations and let the user decide.
- **User provides their own confidence target:** Honor it, even if it's 1.0 (just note if unachievable and why).
- **No thread context available (first message):** Note the cold-start limitation in metadata.

## Validation Gate

Before delivering a DSVSR response, confirm:

- [ ] Every sub-problem has a confidence score with justification
- [ ] Verification changed at least one confidence score (or is documented as confirming all)
- [ ] Global confidence is computed and reported
- [ ] Weaknesses are explicitly stated (not "none found")
- [ ] Metadata block is present and complete
- [ ] Conflicts between sub-answers are resolved or escalated

## Reference Files

- `references/dsvsr-protocol.md` — Worked examples per stage
- `references/confidence-calibration.md` — Calibration methodology and common mis-calibration patterns
- `references/complexity-heuristics.md` — When to activate full DSVSR vs fast path
- `references/recursion-protocol.md` — Thread and attachment scanning protocol
- `references/agent-delegation-patterns.md` — Subagent routing and confidence aggregation

---
**Author:** Javier Montaño | **Last updated:** 2026-03-18
