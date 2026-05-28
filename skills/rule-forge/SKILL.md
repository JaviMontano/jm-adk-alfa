---
name: rule-forge
description: 
  This skill should be used when the user asks to "create a rule", "define a constraint",
  "write a governance rule", "enforce a code standard", or mentions binary Pass/Fail rules,
  enforceability testing, code constraints, linting rules, or rule validation. Creates and
  validates binary governance rules with enforceability testing, scoped examples, and
  self-evaluation. Use this skill whenever the user needs to codify a repeatable constraint
  into a formal rule, even if they don't explicitly ask for "rule-forge". [EXPLICIT]
argument-hint: "constraint description [--scope 'src/**/*.ts'] [--validate path/to/rule.md]"
model: opus
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
version: 1.0.0
---

# Rule Forge

Rules are binary: Pass or Fail. No "try to avoid", no subjective judgment. If you can't express it as Pass/Fail, it's a guideline, not a rule. [EXPLICIT]

## Rule Anatomy

Every rule has five mandatory parts: [EXPLICIT]

| Part | Purpose | Example |
|------|---------|---------|
| Frontmatter | Machine-readable metadata | `description:` + `globs:` |
| Constraint | The binary statement | "No `console.log` in TypeScript production files" |
| Why | The failure it prevents | "Pollutes production logs, leaks internal state" |
| Bad example | Concrete violation | Code snippet showing the problem |
| Good example | Corrected version | Same code with only the violation fixed |

Rules are named `R-kebab-case.md`. For the full template, read `references/output-template.md`. [EXPLICIT]

## Creation Protocol

### Step 1: Define What's Forbidden

Start with the bad pattern. The litmus test: **can a script detect this violation?** [EXPLICIT]

```
Good rule candidates:          Not rules (guidelines): [EXPLICIT]
──────────────────────         ──────────────────────
"No console.log"               "Write clean code"
"Max 50 lines per function"    "Keep functions small"
"No any type in src/"          "Use TypeScript properly"
"All API responses need status" "Design good APIs"
```

If a regex, AST analysis, or linter could find it, it's a rule. If it requires human judgment, it's a guideline. [EXPLICIT]

### Step 2: Define the Scope

Which files does this rule apply to? Scope precision prevents false positives and missed violations. [EXPLICIT]

```
Dangerous:  *                   (everything — almost never correct) [EXPLICIT]
Broad:      **/*.ts             (all TypeScript — sometimes appropriate) [EXPLICIT]
Precise:    src/api/**/*.ts     (API layer only — usually right) [EXPLICIT]
Surgical:   src/api/routes/*.ts (specific directory — very targeted) [EXPLICIT]
```

**Trade-off:** Start narrow. Widening scope later is friction-free; narrowing after adoption causes resistance.

### Step 3: Write the Reasoning

Every rule needs a "Why" section. Rules without reasoning get ignored or deliberately bypassed. [EXPLICIT]

```
Weak:   "Because it's best practice." [EXPLICIT]
Strong: "Untyped API responses silently propagate wrong data structures, [EXPLICIT]
         causing runtime errors that are hard to trace to the API layer."
```

Explain what **failure** this prevents, not what "best practice" it follows. [EXPLICIT]

### Step 4: Provide Paired Examples

Bad example (violation) and Good example (compliance) should be **as close as possible** — ideally the same code with only the violation changed. The smaller the diff, the clearer the rule. [EXPLICIT]

### Step 5: Document Exceptions

Most rules have legitimate exceptions. A test file might need `console.log`. Document these in an "Exceptions" section. Otherwise, the entire rule gets bypassed because of one edge case. [EXPLICIT]

### Step 6: Validate

Check structure, enforceability, and naming: [EXPLICIT]

```bash
python tools/rule-validator.py path/to/R-your-rule.md
python tools/rule-validator.py path/to/rules/          # all rules in directory
python tools/rule-validator.py path/to/rules/ --json    # machine-readable
```

## The Enforceability Test

The most important quality check: [EXPLICIT]

| Question | If "No"... |
|----------|------------|
| Can a script detect violations? | Make constraint more specific, or convert to guideline |
| Is there exactly ONE way to comply? | Narrow scope until compliance is unambiguous |
| Would two independent reviewers always agree on Pass/Fail? | Remove subjective language |

**Red flag words:** "try to", "consider", "prefer", "generally", "appropriate" — these belong in guidelines, not rules.

## Assumptions & Limits

- Rules enforce structure, not intent. A rule can catch `console.log` but not "logging for the wrong reason."
- Cross-file rules (e.g., "every endpoint must have a test") are valid but require multi-file analysis tooling.
- Rules are only as good as their scope. A perfectly written rule with the wrong glob pattern is useless.
- Rule proliferation is a real risk. 50 rules that nobody reads are worse than 10 that everyone follows. Consolidate when possible.

## Edge Cases

- **Overlapping rules:** Two rules targeting the same files with conflicting constraints. Merge into one with clear priority, or narrow scopes until they don't overlap.
- **Subjective criteria:** "Code must be readable" cannot be a rule. Convert to measurable proxy: "Functions must be under 50 lines."
- **Cross-file rules:** Valid but harder to validate. Note that multi-file analysis is required.
- **Rule evolution:** Update in place and use git history. Do NOT create `R-no-console-log-v2.md` — that violates naming conventions and creates confusion.
- **Rules for non-code artifacts:** Same principles apply. A rule like "All SKILL.md files must have frontmatter" is valid and enforceable.
- **Temporary rules:** If a rule is meant to be removed after a migration, document the removal condition and target date in the Why section.

## Validation Gate

Before delivering a rule, confirm: [EXPLICIT]

- [ ] Constraint is binary (Pass/Fail, no gray area)
- [ ] Scope (globs) is specific enough to avoid false positives
- [ ] "Why" explains the failure it prevents, not just "best practice"
- [ ] Bad and Good examples differ by minimal code (only the violation)
- [ ] Exceptions are documented if they exist
- [ ] Rule name follows `R-kebab-case.md` convention
- [ ] The enforceability test passes all 3 questions
- [ ] No subjective language in the constraint

## Reference Files

- `references/output-template.md` — Complete rule template with worked example
- `references/self-evaluation.md` — 10-point quality rubric with red flags
- `references/best-practices.md` — Scope precision, "Power of No", common mistakes

---
**Author:** Javier Montano | **Last updated:** March 18, 2026

## Usage

Example invocations: [EXPLICIT]

- "/rule-forge" — Run the full rule forge workflow
- "rule forge on this project" — Apply to current context

