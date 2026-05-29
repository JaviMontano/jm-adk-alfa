# Contributing to JM Agentic Development Kit

Thank you for your interest in contributing to JM-ADK! This guide will help you get started.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Contribution Types](#contribution-types)
- [Pull Request Process](#pull-request-process)
- [Style Guide](#style-guide)
- [Reporting Issues](#reporting-issues)

## Code of Conduct

### Our Pledge

We are committed to making participation in this project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Positive behavior includes:**

- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Unacceptable behavior includes:**

- Trolling, insulting/derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others' private information without explicit permission
- Other conduct which could reasonably be considered inappropriate

### Enforcement

Project maintainers are responsible for clarifying standards and will take appropriate action in response to unacceptable behavior. Instances of abusive behavior may be reported to **javier@metodologia.info**.

## How to Contribute

### 1. Fork & Clone

```bash
gh repo fork JaviMontano/jm-adk-alfa --clone
cd jm-adk-alfa
```

### 2. Create a Branch

```bash
git checkout -b feat/your-feature-name
# or
git checkout -b fix/your-fix-name
```

### 3. Make Changes

Follow the [Style Guide](#style-guide) and [Project Structure](#project-structure) conventions.

### 4. Test Your Changes

```bash
# Validate skill structure
python3 scripts/validate-skills.py --strict

# Verify documented component counts
python3 scripts/count-components.py --check-docs

# Check local-state and repository boundaries
bash scripts/check-repo-boundaries.sh

# Run safe adversarial guardrail tests
python3 scripts/qa/run-adversarial-tests.py
```

**Definition of Done:** before opening a PR, walk through
[`docs/NO_REGRESSION_CHECKLIST.md`](docs/NO_REGRESSION_CHECKLIST.md). All four
gates above must exit `0` and every checklist item must hold. A change is not
complete until the checklist passes — this is the deterministic acceptance gate.

### 5. Submit a Pull Request

Push your branch and open a PR against `main`.

## Development Setup

### Prerequisites

- Git
- Python 3.10+ (for automation scripts)
- Bash
- Claude Code, Codex, or another compatible agent runner when testing runner-specific integrations

### Local Installation

```bash
# Clone the repository
git clone https://github.com/JaviMontano/jm-adk-alfa.git
cd jm-adk-alfa

# Verify the kit
python3 scripts/count-components.py
python3 scripts/validate-skills.py --strict
bash scripts/check-repo-boundaries.sh

# Optional: run adversarial guardrail tests
python3 scripts/qa/run-adversarial-tests.py
```

## Project Structure

```
jm-adk-alfa/
├── agents/          # 256 specialist agent definitions (.md)
├── commands/        # 260 user-invocable slash commands (.md)
├── skills/          # 524 skill modules (directory/SKILL.md)
├── prompts/         # 256 reusable prompt templates (.md)
├── hooks/           # Session automation hooks
├── references/      # Governance ontology + RAG priming
├── scripts/         # Automation utilities
├── .agent/          # Antigravity Kit compatibility layer
├── .specify/        # Governance documents (Constitution, ADRs, Plans)
├── .claude-plugin/  # Claude Code plugin manifest
├── docs/            # Human-readable documentation
├── ARCHITECTURE.md  # Master index of all components
├── CLAUDE.md        # AI system instructions
└── README.md        # User-facing documentation
```

## Contribution Types

### Adding a New Skill

1. Preview the scaffold:
   ```bash
   python3 scripts/scaffold-skill.py \
     --name your-skill-name \
     --description "One sentence description" \
     --triggers your-skill-name \
     --allowed-tools Read,Grep,Glob,Bash \
     --dry-run
   ```
2. Create the skill only after reviewing the planned files.
3. Follow the MOAT pattern (see any existing skill for reference):
   - Frontmatter: `name`, `author`, `version`, `description`, `allowed-tools`
   - Sections: TL;DR, Procedure (Discover/Analyze/Execute/Validate), Quality Criteria, Anti-Patterns, Related Skills
4. Run `python3 scripts/validate-skills.py --strict` to verify structure
5. Run `bash scripts/generate-pristino-index.sh` when component metadata changes

### Adding a New Agent

1. Create `agents/your-agent-name.md`
2. Follow the agent pattern:
   - Frontmatter: `name`, `description`, `tools`, `model`
   - Sections: Role, Skills (table), Decision Framework, Anti-Patterns, Output Standards
3. Map the agent to 3-5 relevant skills

### Adding a New Command

1. Create `commands/your-command.md`
2. Follow the command pattern:
   - Frontmatter: `description`, `user-invocable: true`
   - Sections: Purpose, Workflow, Arguments, Examples, Related Commands

### Adding a New Prompt

1. Create `prompts/{category}/NN-your-prompt.md`
2. Follow the prompt pattern:
   - Frontmatter: `name`, `category`, `description`, `agents`, `skills`
   - Sections: Context, Prompt (with `{{variables}}`), Expected Output, Variables table

### Improving Documentation

- Fix typos, improve clarity, add examples
- All docs use GitHub-Flavored Markdown
- Keep language accessible — write for developers, not just AI agents

### Reporting Bugs

Use the [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.md) to report issues.

## Pull Request Process

1. **One PR per concern** — Don't mix features, fixes, and docs in one PR
2. **Descriptive title** — Use conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`
3. **Fill the PR template** — Describe what, why, and how to test
4. **Pass validation** — Skills must pass `validate_skills.py`
5. **Update ARCHITECTURE.md** — If you added new agents/skills/commands/prompts
6. **Update CHANGELOG.md** — Add entry under `[Unreleased]`

### Conventional Commit Prefixes

| Prefix | Use Case |
|--------|----------|
| `feat:` | New skill, agent, command, or prompt |
| `fix:` | Bug fix in existing component |
| `docs:` | Documentation changes |
| `refactor:` | Restructuring without behavior change |
| `chore:` | Build scripts, CI, tooling |
| `style:` | Formatting, whitespace |

## Style Guide

### Markdown Files

- Use ATX-style headers (`#`, `##`, `###`)
- One sentence per line (for better diffs)
- Code blocks with language identifiers (````bash`, ````json`, etc.)
- Tables for structured data
- Mermaid diagrams for architecture visualizations

### Skill Frontmatter

```yaml
---
name: kebab-case-name
author: Your Name
version: 1.0.0
description: >
  Multi-line description.
  Trigger: "keyword1, keyword2, keyword3"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
---
```

### Evidence Tags

All factual claims must include evidence tags:

| Tag | Meaning |
|-----|---------|
| `[CODE]` | Verified in source code |
| `[CONFIG]` | Verified in configuration |
| `[DOC]` | Verified in documentation |
| `[INFERENCE]` | Logical deduction |
| `[ASSUMPTION]` | Unverified assumption |

### Naming Conventions

| Component | Convention | Example |
|-----------|-----------|---------|
| Skills | `kebab-case/SKILL.md` | `firebase-setup/SKILL.md` |
| Agents | `kebab-case.md` | `architecture-designer.md` |
| Commands | `kebab-case.md` | `scaffold-firebase.md` |
| Prompts | `NN-kebab-case.md` | `01-analyze-requirements.md` |

## Reporting Issues

### Bug Reports

Use the **Bug Report** issue template. Include:
- Steps to reproduce
- Expected vs actual behavior
- Claude Code version
- Operating system

### Feature Requests

Use the **Feature Request** issue template. Include:
- Problem description
- Proposed solution
- Alternatives considered

## Questions?

- Open a [GitHub Discussion](https://github.com/JaviMontano/jm-adk-alfa/discussions)
- File an [Issue](https://github.com/JaviMontano/jm-adk-alfa/issues)

---

*Made with Claude Code and Tons of Love with the Help of Pristino Agent*
