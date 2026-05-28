---
name: creator-moat-skill
description: 
  This skill should be used when the user asks to "create a production skill",
  "build a moat-level skill", "make a robust skill", "improve skill quality",
  "audit a skill", or mentions skill architecture, skill quality standards,
  skill design patterns, or production-grade skill development. Complements the
  official Anthropic skill-creator by adding structural rigor, quality gates,
  and enterprise patterns. Use alongside or after the official skill-creator
  for skills that need production-grade robustness. [EXPLICIT]
argument-hint: skill-name [description]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Agent
model: opus
context: fork
version: 1.0.0
---

# Skill Creator Moat

Elevate Claude Code skills to production grade. This skill adds structural rigor, quality gates, and enterprise patterns on top of the official Anthropic skill-creator workflow. Use it when a skill needs to be robust enough for team-wide or marketplace distribution. [EXPLICIT]

The official Anthropic skill-creator handles the core loop (draft → test → evaluate → improve → benchmark). This skill focuses on the **quality architecture** that makes the difference between a working skill and a production-grade one. [EXPLICIT]

## When to Use This vs Official Skill-Creator

| Scenario | Use |
|---|---|
| Quick personal skill, vibe-based iteration | Official skill-creator |
| Team-distributed skill needing quality gates | This skill (moat) |
| Marketplace-ready skill with eval infrastructure | Both: official for eval loop, moat for structure |
| Auditing/improving an existing skill | This skill (moat) |
| First-time skill creator learning the ropes | Official skill-creator |

## Assumptions & Limits

- Assumes the user knows what capability to encode — this skill structures it, not invents it
- Assumes the official Anthropic skill-creator plugin is available for the eval/benchmark loop (check: `Glob ~/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/`)
- Skills with side effects (deploy, commit, push) require `disable-model-invocation: true`
- SKILL.md body should stay under 500 lines / ~2,000 words; detailed content goes in references/
- One SKILL.md per skill directory — this is the only required file

## Usage

```
/creator-moat-skill data-migrator "Migrates database schemas with rollback support"
/creator-moat-skill code-reviewer                    # interview mode
/creator-moat-skill --audit ./path/to/skill          # audit existing skill
```

Parse `$1` as skill name (kebab-case, max 64 chars, lowercase letters/numbers/hyphens only) or `--audit` flag. Parse `$2` onward as description or path. If `$2` is absent, conduct a focused interview:

1. What does this skill produce? (artifact type and format)
2. What inputs does it need? (arguments, files, project state)
3. When should Claude invoke it? (specific user phrases — be slightly pushy, Claude under-triggers)
4. Does it have side effects? (file writes, commands, external calls)

## Phase 1: Research & Domain Mapping

Before writing a single line:

1. **Check conflicts**:
   ```
   Glob ~/.claude/skills/*/SKILL.md
   Glob .claude/skills/*/SKILL.md
   ```
   Reject if name collision exists. Suggest merge or rename. [EXPLICIT]

2. **Study golden references**: Read the 2 most relevant official Anthropic skills:
   ```
   Glob ~/.claude/plugins/marketplaces/claude-plugins-official/plugins/*/skills/*/SKILL.md
   ```
   Note their structure, description style, progressive disclosure patterns. [EXPLICIT]

3. **Map the domain** — complete this table BEFORE drafting:

| Dimension | Answer |
|---|---|
| Primary artifact | {file type, format, name pattern} |
| Input sources | {$ARGUMENTS, files, project state, user interview} |
| Failure modes | {missing input, invalid format, ambiguous spec, conflicting requirements} |
| Quality signal | {measurable criteria distinguishing good output from bad} |
| Automation trigger | {specific user phrases — be pushy, Claude under-triggers} |
| Side effects | {files written, commands run, external calls, state changes} |
| Scope boundary | {what this skill does NOT do — name adjacent skills or manual steps} |
| Resources needed | {scripts/, references/, examples/, assets/ — only create what's needed} |

## Phase 2: Draft

### Skill Directory Structure

```
skill-name/
├── SKILL.md              (required — core instructions, <500 lines)
├── references/            (optional — detailed docs loaded as needed)
│   └── patterns.md        (when >300 lines, include a table of contents)
├── examples/              (optional — working code users can copy/adapt)
│   └── sample-output.md
├── scripts/               (optional — executable code for deterministic tasks)
│   └── validate.sh        (must be chmod +x and documented)
└── assets/                (optional — files used in output: templates, icons, fonts)
    └── template.html
```

**Progressive disclosure** (three-level loading):
1. **Metadata** (name + description) — always in context (~100 words)
2. **SKILL.md body** — loaded when skill triggers (<500 lines ideal, can go longer if needed)
3. **Bundled resources** — loaded as needed (unlimited; scripts execute without loading into context)

**Domain organization** — when a skill supports multiple domains/frameworks:
```
cloud-deploy/
├── SKILL.md (workflow + domain selection logic)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```
Claude reads only the relevant reference file. [EXPLICIT]

### Frontmatter

```yaml
---
name: "{kebab-case, max 64 chars}"
description: >
  This skill should be used when the user asks to "{phrase 1}", "{phrase 2}",
  "{phrase 3}", or mentions {keyword}. {One sentence: WHAT it does.}
  Make sure to use this skill whenever the user {broader trigger context},
  even if they don't explicitly ask for "{skill name}". [EXPLICIT]
allowed-tools: "{minimum set — principle of least privilege}"
# Include ONLY when justified:
model: "{opus for complex reasoning, sonnet for balanced, haiku for fast}"
context: fork              # Only if must run in isolated subagent
agent: "{subagent type}"   # Only with context: fork
user-invocable: false      # Only for background knowledge skills
disable-model-invocation: true  # Only for side-effect skills
---
```

**Description rules** (this is THE primary triggering mechanism):
- Third person: "This skill should be used when the user asks to..."
- Include 3-5 specific trigger phrases users would actually say
- Be slightly pushy — Claude tends to under-trigger. Include broader trigger context.
- All "when to use" info goes in the description, not in the body
- Do NOT keyword-stuff, but DO be specific about scenarios

**Trade-off**: `allowed-tools` — too broad = security risk, too narrow = skill breaks on edge cases. Default: Read, Write, Edit, Glob, Grep for generators; add Bash only if the skill runs commands.

### Body Structure

```markdown
# {Name}
{1-2 sentences: value proposition. Explain WHY this skill exists.}

## Assumptions & Limits
{What this skill takes for granted; where it breaks. Be specific.}

## Usage
{2-3 invocation examples with $ARGUMENTS, $1, $2}

## Before {Action}
{Read/Glob/Grep steps for progressive disclosure from references/}

## {Core Process}
{Instructions. Explain WHY things matter — theory of mind > rigid MUSTs. [EXPLICIT]
 Tables > bullets. Code blocks for output templates.}

## Edge Cases
{Non-obvious scenarios with specific handling instructions}

## Example: Good vs Bad
{Concrete comparison — minimum 1 good, 1 bad, with explanation of difference}

## Validation Gate
{Checkbox list of ≥5 testable criteria — no subjective items}

## Additional Resources
{Pointers to references/, examples/, scripts/ — explain when to read each}
```

### Writing Rules

| Rule | Rationale |
|---|---|
| Imperative form ("Read the file") | Removes ambiguity, shorter, consistent |
| Third-person in description | Anthropic standard for skill routing |
| Explain WHY, not just WHAT | Models respond better to reasoning than rigid MUSTs |
| Tables for structured data | Faster to scan than bullet lists |
| Code blocks for output templates | Shows exact expected format |
| One concern per section | Prevents section bloat |
| No ALWAYS/NEVER in caps | Reframe as reasoning; caps ≠ emphasis for LLMs |
| Reference files from SKILL.md | Tell Claude what each file contains and when to read it |

**Anti-patterns to avoid**:
- Keyword stuffing in description — be specific, not encyclopedic
- Everything in SKILL.md (>500 lines without references/) — use progressive disclosure
- Second person ("You should...") — use imperative ("Parse the input")
- Unreferenced resources — Claude won't know they exist
- Broken examples — test all examples before shipping

## Phase 3: Quality Audit

Whether creating new or improving existing, audit against this rubric:

### Structural Audit (pass/fail)

- [ ] One SKILL.md file in the top-level skill directory
- [ ] Frontmatter has `name` and `description` (both required)
- [ ] Description uses third person with specific trigger phrases
- [ ] Description is slightly "pushy" to combat Claude's under-triggering
- [ ] Body uses imperative/infinitive form throughout (no "you should")
- [ ] SKILL.md body ≤ 500 lines; detailed content in references/
- [ ] All referenced files (references/, examples/, scripts/) actually exist
- [ ] Scripts are executable (`chmod +x`) and documented
- [ ] No duplicate information across SKILL.md and reference files

### Content Audit (1-10 scale)

| Dimension | 10 means | Common failure |
|---|---|---|
| Trigger accuracy | Description causes skill to fire on right prompts, not wrong ones | Vague description, missing trigger phrases |
| Completeness | All required sections present with substantive content | Missing validation gate, placeholder text |
| Clarity | Zero ambiguity; a different Claude instance follows perfectly | Vague instructions, missing format specs |
| Robustness | Handles missing/invalid input with helpful error guidance | Crashes on missing args, no edge cases |
| Efficiency | No unnecessary context loading, reads, or bloat | Reading files it doesn't need |
| Value density | Every sentence adds practical value | Filler, redundancy, restating the obvious |

**Decision rule**: Score < 7 on ANY dimension → mandatory revision. Average < 8 → recommended revision.

## Phase 4: Improvement Patterns

Based on audit findings, apply these proven patterns:

1. **Script extraction**: If test runs independently wrote similar helper code → bundle it in scripts/. This saves every future invocation from reinventing the wheel. [EXPLICIT]

2. **Reference extraction**: SKILL.md approaching 500 lines → move detailed content to references/. For large reference files (>300 lines), include a table of contents. [EXPLICIT]

3. **Theory of mind**: Replace rigid "MUST/ALWAYS/NEVER" instructions with reasoning that explains WHY. Models are smart — they respond better to understanding than commands. [EXPLICIT]

4. **Generalize from specifics**: Skills run millions of times across diverse prompts. Avoid overfitting to test cases. If an instruction needs caps-lock emphasis, it probably needs better reasoning instead. [EXPLICIT]

5. **Lean the prompt**: Read test transcripts, not just outputs. If the skill makes the model waste time on unproductive steps, remove those instructions. [EXPLICIT]

6. **Look for repeated work**: If all test cases independently wrote similar helper scripts, that's a signal to bundle the script in scripts/. [EXPLICIT]

## Phase 5: Production Packaging

### For standalone skills (personal or project)

Place in `~/.claude/skills/skill-name/` (personal) or `.claude/skills/skill-name/` (project). [EXPLICIT]

### For plugin distribution

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json        # Only plugin.json goes here
├── skills/
│   └── skill-name/
│       ├── SKILL.md
│       ├── references/
│       ├── examples/
│       └── scripts/
├── commands/              # User-invocable slash commands
├── agents/                # Subagent definitions
└── hooks/                 # Event handlers
```

### For .skill ZIP distribution

```bash
cd /path/to/skill-name
zip -r skill-name.skill . [EXPLICIT]
# Structure inside ZIP: skill-name/SKILL.md (flat, NOT skill-name/skill-name/SKILL.md)
```

## Meta-Validation Gate

Before declaring a skill production-ready:

- [ ] One SKILL.md in the top-level skill directory (not nested deeper)
- [ ] Frontmatter has name, description with third-person trigger phrases
- [ ] Description includes 3-5 specific user phrases and is slightly "pushy"
- [ ] Body uses imperative form throughout (no second person)
- [ ] Body ≤ 500 lines; detailed content in references/ with clear pointers
- [ ] ≥1 concrete good-vs-bad example with explanation
- [ ] Validation gate with ≥5 testable criteria (no subjective items)
- [ ] Assumptions & Limits section present and specific
- [ ] Edge Cases section present with ≥3 scenarios
- [ ] All referenced files exist and are not duplicated
- [ ] Progressive disclosure: metadata → body → resources
- [ ] No malware, exploit code, or security-compromising content
- [ ] Skill's intent would not surprise the user if described

---
**Author:** Javier Montaño | **Last updated:** 2026-03-12
