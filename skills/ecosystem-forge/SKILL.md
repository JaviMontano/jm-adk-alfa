---
name: ecosystem-forge
description: 
  This skill should be used when the user asks to "bootstrap an ecosystem",
  "audit artifact consistency", "create a coordinated system of skills",
  "verify ecosystem integrity", or mentions ecosystem forge, artifact
  coordination, cross-artifact validation, or governance bootstrap. It
  verifies, repairs, and bootstraps interconnected artifact ecosystems
  including skills, rules, workflows, and naming conventions as coordinated
  systems. Use this skill whenever 3+ interrelated artifacts need to work
  together as a system, even if they don't explicitly ask for "ecosystem
  forge".
argument-hint: "domain-name or path-to-ecosystem [--mode bootstrap|audit|repair] [--pattern governance|workflow|skill]"
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

# Ecosystem Forge

Individual forges (prompt-forge, rule-forge, workflow-forge) create artifacts. Ecosystem-forge coordinates them into a coherent system. Use it when you need 3+ interrelated artifacts working together. [EXPLICIT]

## When to Use This vs Other Skills

| Need | Skill |
|------|-------|
| Create a single skill | skill-creator |
| Create a single rule | rule-forge |
| Create a single workflow | workflow-forge |
| Create a coordinated system of skills + rules + workflows | **ecosystem-forge** |
| Bootstrap governance for a new project | **ecosystem-forge** |
| Audit an existing ecosystem for consistency | **ecosystem-forge** |

**Minimum threshold:** If the request involves fewer than 3 artifacts, redirect to the appropriate individual forge.

## Ecosystem Structure

```
my-domain/
├── skills/
│   └── my-skill/
│       ├── SKILL.md
│       ├── references/
│       └── tools/
├── rules/
│   ├── R-constraint-one.md
│   └── R-constraint-two.md
├── workflows/
│   ├── create-artifact.md
│   └── validate-output.md
```

## The Creation Process

### Phase 1: Domain Mapping

Before creating anything, answer: [EXPLICIT]

1. **What problem does this ecosystem solve?** (One sentence.)
2. **What artifact types does it need?**
   - Skills: complex capabilities requiring domain knowledge
   - Rules: binary constraints that must always hold
   - Workflows: repeatable multi-step processes
3. **How do artifacts relate?** Which workflows use which skills? Which rules constrain which artifacts?

### Phase 2: Name Everything First

Use naming-and-slugging conventions to name all artifacts before creating them. Consistent naming makes cross-referencing reliable. [EXPLICIT]

```
Domain: API Development [EXPLICIT]
├── Skill: api-builder
├── Rules: R-no-inline-sql, R-typed-responses, R-auth-required
├── Workflows: create-endpoint, validate-api, deploy-api
```

### Phase 3: Create in Dependency Order

Order matters because later artifacts reference earlier ones: [EXPLICIT]

1. **Rules first** — they define constraints everything else must follow. [EXPLICIT]
2. **Skills second** — they reference rules and encode domain knowledge. [EXPLICIT]
3. **Workflows last** — they orchestrate skills and enforce rules during execution. [EXPLICIT]

Each artifact follows its forge's standards: rule-forge for rules, skill-creator for skills, workflow-forge for workflows. [EXPLICIT]

### Phase 4: Verify Integration

After all artifacts exist, run the integration checklist: [EXPLICIT]

- [ ] All artifacts follow kebab-case naming
- [ ] Cross-references between artifacts resolve (no dangling references)
- [ ] No two rules impose contradictory constraints on the same scope
- [ ] Every workflow's prerequisites are satisfiable
- [ ] No orphans: every artifact is referenced by at least one other or is a documented entry point

## Ecosystem Patterns

### Governance-First

Best for regulated or quality-critical domains. [EXPLICIT]

```
1. Define all rules (forbidden/required behaviors)
2. Create skills that inherently comply with rules
3. Create workflows that enforce rules during execution
```

**Trade-off:** Thorough but slow to bootstrap. Rules may be over-specified before real usage reveals what matters.

### Workflow-First

Best for process automation. [EXPLICIT]

```
1. Map the manual process into a workflow
2. Identify steps needing specialized knowledge → create skills
3. Identify invariants that must always hold → create rules
```

**Trade-off:** Practical and grounded, but may miss cross-cutting constraints that span multiple workflows.

### Skill-First

Best for capability building. [EXPLICIT]

```
1. Create the core skill with references and tools
2. Add rules to prevent common mistakes
3. Add workflows for common usage patterns
```

**Trade-off:** Fast to start delivering value, but governance is retrofitted. Works well for greenfield projects.

## Integration Quality Checks

| Check | What to Verify |
|-------|----------------|
| Naming consistency | All artifacts follow the same naming conventions |
| Reference integrity | No broken cross-references between artifacts |
| Rule coverage | Rules cover critical paths in the domain |
| Workflow completeness | Key user journeys have corresponding workflows |
| No redundancy | No two artifacts do the same thing |
| Scope alignment | Rule scopes match the files workflows actually create |

## Assumptions & Limits

- Ecosystem-forge coordinates; it does not replace individual forges. Each artifact must still meet its forge's quality bar independently.
- Cross-ecosystem dependencies (ecosystem A depends on ecosystem B) should be documented explicitly. Implicit dependencies break silently.
- Ecosystem verification is structural, not semantic. It checks that references resolve, not that the logic is correct.
- Large ecosystems (20+ artifacts) benefit from a dependency diagram. For smaller ones, the checklist suffices.

## Edge Cases

- **Adding to an existing ecosystem:** Audit current state first. Check naming consistency, rule conflicts, and workflow coverage before adding new artifacts. New additions must not break existing cross-references.
- **Single-artifact requests disguised as ecosystems:** If the user asks for "a complete system" but only one artifact is needed, explain this and redirect to the appropriate forge.
- **Conflicting rules discovered during integration:** Do not silently pick one. Surface the conflict, explain the trade-off, and let the user decide which constraint takes priority.
- **Partial ecosystem (only rules, no workflows):** This is valid. Not every ecosystem needs all artifact types. Document which types are intentionally absent and why.
- **Ecosystem for a domain you don't fully understand:** Front-load discovery in Phase 1. Ask clarifying questions before creating artifacts. A wrong ecosystem is worse than no ecosystem.

## Validation Gate

Before declaring an ecosystem complete, confirm: [EXPLICIT]

- [ ] All artifacts pass their individual forge's validation (rule-forge, workflow-forge, etc.)
- [ ] Integration checklist (Phase 4) passes with zero failures
- [ ] Dependency order was respected during creation
- [ ] No artifact references a non-existent artifact
- [ ] Naming follows kebab-case consistently across all artifact types
- [ ] At least one workflow exercises the core skill(s) end-to-end

## Reference Files

- `references/ecosystem-checklist.md` — Complete integration verification checklist
- `references/artifact-relationships.md` — How to map dependencies between artifacts

---
**Author:** Javier Montano | **Last updated:** March 18, 2026
