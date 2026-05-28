---
name: naming-and-slugging
description: 
  This skill should be used when the user asks to "generate a slug", "rename files to kebab-case",
  "audit naming conventions", "clean up filenames", or "validate a name". Also triggers on mentions
  of slug generation, kebab-case, filename linting, registry audit, or naming patterns. Use this
  skill even if the user only has a single file to rename — the full naming protocol ensures
  consistency across the project. [EXPLICIT]
argument-hint: "name-to-slug or path-to-audit [--clean] [--validate] [--strict] [--json]"
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

# Naming & Slugging

Every artifact should be findable via search, safe for URLs and filesystems, and self-describing. [EXPLICIT]

## Quick Reference

### Slug Generation
```
Input                        →  Output [EXPLICIT]
"My New Component"           →  my-new-component
"api_client_FINAL.ts"        →  api-client-final.ts
"  Hllo Wrld!! "            →  hello-world
```

### Clean Mode (strips versions and status)
```
Input                        →  Output [EXPLICIT]
"My New Component v2"        →  my-new-component
"new-api-client-v3.ts"       →  api-client.ts
"old-dashboard-final.md"     →  dashboard.md
```

### Entity Naming Patterns

| Entity Type | Pattern | Example |
|-------------|---------|---------|
| Skill | `kebab-case/` | `naming-and-slugging/` |
| Workflow | `verb-noun.md` | `create-component.md` |
| Rule | `R-kebab-case.md` | `R-no-console-log.md` |
| Document | `kebab-case.md` | `architecture-overview.md` |

## Core Principles

**Names describe content, not status or version.** Someone seeing the filename in a listing should immediately understand what's inside.

- **Slug:** URL-friendly string — lowercase letters, numbers, hyphens only. No underscores, no spaces, no special characters.
- **Kebab-case:** Words separated by hyphens (`my-file-name`). Reads well, URL-safe, works on all filesystems including case-sensitive.
- **Semantic naming:** Name reflects what it *is*, not where it came from. `api-client.ts` not `new-api-client-v2-final.ts`. Versions belong in git, not filenames.

## Core Process

### Step 1: Identify Entity Type

Determine if it's a skill, workflow, rule, document, or general file. Each type has a specific pattern (see table above). [EXPLICIT]

For detailed conventions per entity type, read `references/naming-patterns.md`. [EXPLICIT]

### Step 2: Generate the Slug

**Basic slug** (normalize characters):
```bash
python tools/slugger.py "My Raw Name Here"
# → my-raw-name-here
```

**Clean name** (normalize + strip versions/status):
```bash
python tools/slugger.py --clean "new-api-client-v2-final"
# → api-client
```

The `--clean` flag removes: version markers (`v1`, `v2`), status prefixes (`new-`, `old-`, `final-`, `draft-`, `temp-`, `wip-`), and trailing noise (`final`, `copy`). [EXPLICIT]

### Step 3: Validate

```bash
python tools/slugger.py --validate "my-component"
# → 'my-component' is valid.

python tools/slugger.py --validate "my_Bad_Name-v2"
# → Issues: uppercase, underscores, version marker → suggested: my-bad-name
```

Validation catches: uppercase, underscores, spaces, invalid characters, consecutive hyphens, version markers, status prefixes, excessive length. [EXPLICIT]

### Step 4: Audit a Project

```bash
python tools/registry-linter.py /path/to/project
python tools/registry-linter.py /path/to/project --strict    # warnings = errors
python tools/registry-linter.py /path/to/project --json      # machine-readable
```

## Self-Correction Triggers

When encountered during any file operation, apply automatically: [EXPLICIT]

| Pattern Detected | Action |
|------------------|--------|
| Underscore in filename | Replace with hyphen |
| Version marker (`v1`, `v2`, `final`) | Remove; note version should be git tag |
| Uppercase letters | Convert to lowercase |
| More than 5 words | Abbreviate while preserving meaning |
| Status prefix (`new-`, `old-`, `draft-`) | Remove the prefix |
| Consecutive hyphens | Collapse to single hyphen |

## Antipatterns and Fixes

| Problem | Bad | Good | Why |
|---------|-----|------|-----|
| Versioning | `api-client-v2.ts` | `api-client.ts` + git tag | Versions belong in VCS |
| Status markers | `new-component.tsx` | `component.tsx` | "New" is relative, temporary |
| Underscores | `my_file_name.md` | `my-file-name.md` | Kebab-case is web standard |
| Uppercase | `MyComponent.tsx` | `my-component.tsx` | Lowercase is universal, grep-friendly |
| Deep nesting | `.../v1/drafts/file.md` | `.../file.md` | Flat structures are navigable |
| Too long | `user-authentication-service-handler.ts` | `auth-handler.ts` | Aim for 2-4 words |
| Too cryptic | `usr-auth-svc.ts` | `user-auth.ts` | Descriptive, not abbreviated |
| Compound ext | `component.test.tsx` | Keep as-is | Compound extensions are semantic, not violations |

## Assumptions & Limits

- Kebab-case is the universal default. Some ecosystems (React components, Python modules) have their own conventions. When working in such ecosystems, note the deviation and follow the ecosystem's standard.
- The `--clean` flag is opinionated. It removes version markers because versions belong in git. If the user explicitly wants versions in filenames (e.g., API versioning: `v1/routes.ts`), respect that.
- Registry linting is structural. It checks naming patterns, not whether names are semantically meaningful.
- Renaming existing files can break imports and references. Always audit downstream dependencies before bulk renaming.

## Edge Cases

- **Acronyms:** `API`, `HTML`, `CSS` become `api`, `html`, `css` in slugs. Do not hyphenate individual letters (`a-p-i` is wrong).
- **Numbers:** Valid in slugs. `step-1`, `v2-migration` are fine. Version markers (`v2`) are only stripped in `--clean` mode.
- **Non-Latin characters:** Transliterate to ASCII equivalents. `caf` becomes `cafe`, `uber` becomes `uber`.
- **File already correctly named:** Validation should confirm and move on. Do not rename for the sake of renaming.
- **Compound extensions:** `.test.ts`, `.module.css`, `.stories.tsx` are semantic. Do not treat the first dot as the extension boundary.
- **Platform-specific constraints:** Windows has a 260-char path limit. macOS is case-insensitive by default. Account for target platform.
- **Bulk renaming with git:** Use `git mv` to preserve history. Never `mv` + `git add` for tracked files.

## Validation Gate

Before delivering a naming recommendation or rename operation, confirm: [EXPLICIT]

- [ ] All names use lowercase kebab-case (or documented exception)
- [ ] No version markers in filenames (or user explicitly requested them)
- [ ] No status prefixes (`new-`, `old-`, `draft-`)
- [ ] Names are 2-4 words (or justified exception for longer names)
- [ ] No consecutive hyphens
- [ ] Compound extensions preserved (`.test.ts`, `.module.css`)
- [ ] Downstream references checked before any rename
- [ ] Entity type pattern applied (skills, rules, workflows follow their conventions)

## Reference Files

- `references/naming-patterns.md` — Detailed conventions per entity type, edge cases (acronyms, numbers, compound extensions), canonical slug algorithm

---
**Author:** Javier Montaño | **Last updated:** 2026-03-12

## Usage

Example invocations: [EXPLICIT]

- "/naming-and-slugging" — Run the full naming and slugging workflow
- "naming and slugging on this project" — Apply to current context

