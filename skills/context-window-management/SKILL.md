---
name: context-window-management
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Token budgeting, context compression, priority-based summarization. [EXPLICIT]
  Trigger: "context window management"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---
# Context Window Management

> "Method over hacks."

## Purpose

Manages context-window pressure with deterministic token budgets, priority tiers,
compression rules, and eviction boundaries. It protects high-priority session
state while reducing lower-priority context into verifiable summaries or
references. [EXPLICIT]

## When to Activate

- The user asks for context window management, token budgeting, context trimming,
  compression, summarization priority, or what to preserve before a large task.
- A session is approaching context limits and needs an explicit keep/compress/evict
  plan.
- A handoff or compact operation needs a deterministic context budget report.

Do not activate for browser window sizing, UI layout windows, operating-system
window management, or generic text summarization without context-budget pressure.

## Deterministic Resources

- `assets/budget-policy.json` defines budget fields and response reserve rules.
- `assets/priority-policy.json` defines P0/P1/P2/P3 retention tiers.
- `assets/compression-policy.json` defines allowed compression methods and
  preservation requirements.
- `assets/eviction-policy.json` defines safe eviction order and P0 protection.
- `assets/report-contract.json` defines the machine-checkable budget report.
- `scripts/validate_context_window_report.py` validates reports offline.
- `scripts/check.sh` runs deterministic positive and negative fixtures.

## Procedure

### Step 1: Discover

1. List context items with stable IDs, source names, and estimated token counts.
2. Record `max_context_tokens`, `reserved_response_tokens`, and computed
   `available_context_tokens`.
3. Classify each context item as P0, P1, P2, or P3.

### Step 2: Analyze

1. Sum current estimated tokens.
2. Keep all P0 items in full.
3. Prefer compressing P2/P3 before evicting.
4. Evict only the lowest-priority eligible items when compression is insufficient.
5. Require compression output to preserve IDs, paths, decisions, blockers,
   validation evidence, and open questions when present.

### Step 3: Execute

Create a plan with:

- context budget
- item-level keep/compress/evict actions
- compression method and before/after estimates
- eviction reasons
- final post-plan token estimate
- Guardian decision

### Step 4: Validate

- `available_context_tokens = max_context_tokens - reserved_response_tokens`.
- `post_plan_estimated_tokens <= available_context_tokens`.
- P0 items are never evicted.
- Compression never increases estimated tokens.
- Compression preserves required durable facts.
- Eviction order starts at P3, then P2, then P1 only with Guardian warning.

## Priority Tiers

| Tier | Meaning | Default Action |
|---|---|---|
| P0 | Active user instructions, repo status, open PR/blocker, current branch, validation evidence. | keep |
| P1 | Active task files, recently edited code, current skill contract. | keep or structured-summary |
| P2 | Supporting docs, examples, adjacent context. | compress |
| P3 | Historical or redundant context. | reference or evict |

## Quality Criteria

- [ ] Budget fields are explicit and arithmetically consistent.
- [ ] Every item has ID, priority, estimate, action, rationale, and evidence tag.
- [ ] P0 items are kept.
- [ ] Compression methods are allowed and reduce token estimates.
- [ ] Compression preservation fields are non-empty.
- [ ] Eviction targets lowest-priority eligible items first.
- [ ] Final estimate fits the available budget.
- [ ] Machine report passes `bash skills/context-window-management/scripts/check.sh`.

## Usage

Example invocations:

- `/context-window-management`
- `Plan context trimming before this large refactor.`
- `Create a keep/compress/evict plan for these sources with an 8000-token budget.`

## Assumptions & Limits

- Token counts are estimates unless a tokenizer is explicitly provided. [EXPLICIT]
- The skill does not delete source files or mutate project state. [EXPLICIT]
- The skill does not replace user confirmation for dropping active context. [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|---|---|
| Missing token estimates | Block or request estimates. |
| Over budget after compression | Evict eligible P3/P2 items or block. |
| P0 proposed for eviction | Block. |
| Compression loses IDs or decisions | Block. |
| Browser window request | Do not activate. |
