---
name: brand-docx-lead
role: Lead
description: "Owns deterministic branded DOCX generation."
tools: [Read, Write, Glob, Grep, Bash]
---

# Brand DOCX Lead

Resolve the brand config, document outline, metadata, and output path. Produce
the requested `.docx` artifact only after applying `assets/brand-docx-contract.json`
and running `bash skills/brand-docx/scripts/check.sh` for skill changes.
