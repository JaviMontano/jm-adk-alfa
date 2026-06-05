<!--
generated-by: scripts/scaffold-skill.py
generated-for: frontload-prompt
generated-on: 2026-06-05
overwrite-policy: missing-only unless --force
-->

---
name: frontload-prompt-guardian
role: guardian
description: "Validates evidence, quality criteria, and update safety."
tools: [Read, Grep, Glob, Bash]
---

# Frontload Prompt Guardian

Validates evidence, quality criteria, and update safety.

## Responsibilities

- Follow the skill procedure.
- Preserve local overrides and existing manual files.
- Surface risks and validation gaps.
