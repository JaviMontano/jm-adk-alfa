---
name: continuous-learning
author: JM Labs (Javier Montaño)
version: 1.0.0
description: 
  Extract reusable insights from Socratic debates and discoveries. Capture patterns
  in insights/domain.md. Propose constitution amendments when recurring ambiguity detected. [EXPLICIT]
  Consult insights before initiating new debates. Constitution XVII. [EXPLICIT]
  Trigger: "extract insight", "learn from debate", "continuous learning", "prevent re-debate", "insights"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Write
  - Edit
---

# Continuous Learning Loop

> "A project that doesn't learn from its own decisions is condemned to re-debate them."

## TL;DR

Implements Constitution XVII: every debate and discovery produces reusable insights captured in `insights/<domain>.md`. Before new debates, consult existing insights. When recurring ambiguity detected, propose constitution amendments. The project compounds knowledge — it never re-debates a settled class of decision. [EXPLICIT]

Use deterministic assets in `assets/` for insight taxonomy, evidence, duplicate handling, amendment gates, update plans, and report shape. When producing a JSON learning report, validate it offline with `bash skills/continuous-learning/scripts/check.sh`. [EXPLICIT]

## Procedure

### Step 1: Discover
- After any Socratic debate or significant decision, read the debate record
- Identify the three outputs: (1) direct answer, (2) refinements to original question, (3) coverage gaps
- Check `insights/` for existing patterns in the same domain
- Determine if this is a new pattern or refinement of existing one

### Step 2: Analyze
- Extract the reusable decision pattern (abstract from specific case)
- Classify domain: `universal`, `security`, `frontend`, `backend`, `testing`, `deployment`, `governance`
- Identify trigger conditions (when should future agents apply this insight?)
- Map to constitutional anchor (which principle does this insight support?)
- Check frequency: has this class of question appeared 3+ times? → constitution amendment candidate

### Step 3: Execute
- Write insight to `insights/<domain>.md`:
  ```markdown
  ### Insight: {title}
  - **Origin**: Debate on {topic} ({date})
  - **Pattern**: {reusable decision pattern}
  - **Rationale**: {why this is the right default}
  - **Trigger**: {when to apply this insight}
  - **Constitutional Anchor**: Principle {N}
  - **Status**: active | tentative | superseded
  ```
- If 3+ debates in same class → draft constitution amendment in `.specify/adr/`
- Update `insights/README.md` index with new entry
- Cross-reference debate record with insight

### Step 4: Validate
- Insight is abstract enough to apply beyond the original case
- Trigger conditions are specific enough to match future queries
- Constitutional anchor is correct
- No duplicate insight exists (check before writing)
- If amendment proposed: rationale is strong, scope is clear

## Quality Criteria

- [ ] Three outputs extracted from every debate (answer, refinements, gaps)
- [ ] Insight written to correct domain file
- [ ] Trigger conditions are actionable
- [ ] Constitutional anchor identified
- [ ] `insights/README.md` updated
- [ ] Frequency check performed (3+ → amendment)
- [ ] No duplicate insights
- [ ] Evidence tags applied
- [ ] Prior insight search recorded
- [ ] Amendment candidates include recurrence evidence
- [ ] JSON report passes `scripts/check.sh` when produced

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do This Instead |
|-------------|-------------|-----------------|
| Skipping insight extraction | Knowledge lost, same debates repeat | Extract after every significant decision |
| Over-specific insights | Can't apply to future cases | Abstract the pattern from the specifics |
| Never amending constitution | Ambiguity keeps recurring | Amend when 3+ debates hit same class |
| Not consulting insights before debate | Wasted effort re-debating | Always check `insights/` first |

## Related Skills

- `socratic-debate` — Produces the debates that feed insights
- `integrity-chain-validation` — Insights improve chain compliance
- `repository-organization` — Insights files follow indexability rules (XVIII)

## Usage

Example invocations:

- "/continuous-learning" — Run the full continuous learning workflow
- "continuous learning on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
