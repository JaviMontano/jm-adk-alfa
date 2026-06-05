---
name: audit-content-quality-meta
type: meta
version: 2.0.1
description: "Meta-prompt for Audit Content Quality routing."
---

# Audit Content Quality Meta Prompt

Use `assets/activation-policy.json` and `SKILL.md ## When To Activate` before
activating this skill.

Activate for requests to audit, score, rank, compare, or improve `SKILL.md`
content quality, weakest skills, plugin quality score, or rubric-based skill
content assessment.

Do not activate for security review, code review, factuality audit, generic
website/article content quality, design critique, or grammar-only review. If no
target path is supplied, return `needs_clarification` and ask for
`plugin_root_or_skill_paths`.
