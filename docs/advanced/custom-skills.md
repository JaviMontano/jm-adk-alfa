# Creating Custom Skills

How to extend JM-ADK with your own skills.

## Skill Anatomy

Every skill lives in `skills/{skill-name}/SKILL.md` and follows the MOAT pattern:

```
skills/
└── my-custom-skill/
    └── SKILL.md
```

### Frontmatter (Required)

```yaml
---
name: my-custom-skill
author: Your Name
version: 1.0.0
description: >
  One-paragraph description of what this skill does and when to use it.
  Trigger: "keyword1, keyword2, keyword3"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Write
  - Edit
---
```

| Field | Purpose |
|-------|---------|
| `name` | Kebab-case identifier, must match directory name |
| `author` | Attribution |
| `version` | Semantic version |
| `description` | What the skill does + trigger keywords for routing |
| `allowed-tools` | Which Claude Code tools this skill can use |

### Body Structure

```markdown
# Skill Title

> "Optional inspirational quote"

## TL;DR

One paragraph: what this skill does, when to use it, what it produces.

## Procedure

### Step 1: Discover
- Read existing files and context
- Identify constraints and requirements
- Ask clarifying questions if needed

### Step 2: Analyze
- Evaluate options and trade-offs
- Select approach with evidence
- Document decisions

### Step 3: Execute
- Implement the solution
- Follow coding standards
- Add evidence tags to all claims

### Step 4: Validate
- Verify against quality criteria
- Run relevant checks
- Document any gaps

## Quality Criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do This Instead |
|-------------|-------------|-----------------|
| Pattern 1 | Reason | Alternative |

## Related Skills

- `skill-a` — When to use instead
- `skill-b` — Complements this skill
```

## Step-by-Step: Create a Skill

### 1. Define the Scope

Ask yourself:
- What **one thing** does this skill do? (single responsibility)
- When should the AI **route** to this skill? (trigger keywords)
- What **tools** does it need? (minimal set)
- What does the **output** look like? (expected deliverable)

### 2. Preview the Scaffold

```bash
python3 scripts/scaffold-skill.py \
  --name my-custom-skill \
  --description "One-paragraph description of what this skill does" \
  --triggers my-custom-skill,keyword1 \
  --allowed-tools Read,Grep,Glob,Bash \
  --dry-run
```

Review the planned files before creating anything.
The scaffold refuses duplicate skill slugs unless `--force` is explicit.

### 3. Create the Skill

```bash
python3 scripts/scaffold-skill.py \
  --name my-custom-skill \
  --description "One-paragraph description of what this skill does" \
  --triggers my-custom-skill,keyword1 \
  --allowed-tools Read,Grep,Glob,Bash
```

Then refine `skills/my-custom-skill/SKILL.md` following the MOAT pattern above.

### 4. Validate

```bash
python3 scripts/validate-skills.py --strict
```

This checks:
- Frontmatter has all required fields
- `name` matches directory name
- `allowed-tools` only contains valid tools
- Body has required sections (Procedure, Quality Criteria)
- Evals and knowledge graph JSON are valid

### 5. Update the Index

```bash
bash scripts/generate-pristino-index.sh
```

This rebuilds `PRISTINO-INDEX.md` when component metadata changes.

### 6. Test It

```bash
python3 scripts/qa/run-adversarial-tests.py
```

Then test routing in your chosen runner by mentioning the skill triggers.

## Real Example: `email-templates` Skill

```yaml
---
name: email-templates
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Creates responsive HTML email templates compatible with major email clients
  (Gmail, Outlook, Apple Mail). Uses table-based layouts for maximum compatibility.
  Trigger: "email template, newsletter, email HTML, transactional email"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Email Templates

> "The inbox is the most personal screen on any device."

## TL;DR

Creates responsive HTML email templates using table-based layouts for
cross-client compatibility. Supports transactional emails, newsletters,
and marketing campaigns. All templates pass Litmus/Email on Acid validation.

## Procedure

### Step 1: Discover
- Read existing email templates in the project
- Identify the email type (transactional, marketing, notification)
- Check brand guidelines (colors, fonts, logo URLs)
- Determine target email clients

### Step 2: Analyze
- Select layout pattern (single column, multi-column, hero)
- Plan responsive breakpoints (600px max-width standard)
- Map content blocks to table structure
- Identify dynamic variables ({{user_name}}, {{order_id}})

### Step 3: Execute
- Write HTML with table-based layout
- Inline all CSS (no external stylesheets)
- Add MSO conditionals for Outlook
- Include plain-text fallback
- Use web-safe fonts with fallbacks

### Step 4: Validate
- Check: all CSS is inlined
- Check: images have alt text
- Check: links have tracking parameters
- Check: renders at 600px and 320px widths
- Check: no JavaScript (stripped by all clients)

## Quality Criteria

- [ ] Table-based layout (no div-based)
- [ ] All CSS inlined
- [ ] Max-width: 600px
- [ ] Images have alt text and fixed dimensions
- [ ] Web-safe font stack
- [ ] MSO conditionals for Outlook
- [ ] Preheader text included
- [ ] Unsubscribe link present (marketing emails)

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do This Instead |
|-------------|-------------|-----------------|
| CSS classes | Stripped by Gmail | Inline styles |
| `<div>` layout | Broken in Outlook | `<table>` layout |
| Web fonts | Not supported | Web-safe stack |
| JavaScript | Stripped by all clients | Static HTML only |
| Background images | Outlook ignores | VML fallback |

## Related Skills

- `landing-pages` — For web landing pages (not email)
- `html-semantic` — For semantic web pages
- `css-architecture` — For web CSS (email CSS is different)
```

## Skill Design Principles

1. **Single Responsibility** — One skill, one job. If it does two things, split it.
2. **Minimal Tools** — Only request the tools you actually need.
3. **Evidence-Based** — Every claim in the output gets an evidence tag.
4. **Discoverable** — Trigger keywords should match how developers think about the problem.
5. **Self-Contained** — A skill should work without reading other skills (but can reference them).
6. **Validate Everything** — Step 4 (Validate) is not optional.

## Skill Routing

The `skill-router` agent uses BM25 full-text search to match user requests to skills. Your `description` field is the primary search target, with `name` and trigger keywords as boosted terms.

Tips for good routing:
- Include **synonyms** in your trigger keywords ("email template, newsletter, email HTML")
- Describe the **output**, not just the input ("Creates responsive HTML email templates")
- Mention the **technology** ("table-based layouts, cross-client compatibility")

---

*Made with Claude Code and Tons of Love with the Help of Pristino Agent*
