# Domain Knowledge - Prompt Forge

## Overview

Prompt Forge is a deterministic prompt lifecycle skill for creating, reviewing, evolving, repairing, and porting system prompts.

## Evidence Policy

- Tag source-backed facts as provided or cited.
- Tag assumptions explicitly.
- Do not create current platform claims without a dated source.
- Do not invent business policies, source IDs, tools, or platform capabilities.

## Integration Points

- Use `prompt-engineering` for pattern selection and instruction package design.
- Use `prompt-creator` for durable prompt file generation after the forge packet is approved.
- Use `agent-constitution-creator` when the user needs agent identity, authority, and governance instead of a prompt artifact.
