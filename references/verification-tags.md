# Verification Tags

Inline provenance tags for claims and outputs. Two homologated families: the
Jarvis OS runbook set (operator-facing) and the Alfa core set (kit-facing).
Mark every non-obvious claim; for `{SUPUESTO}`/`{POR_CONFIRMAR}` propose the
next step that would verify it.

## Jarvis OS set (operator)

| Tag | Meaning |
|---|---|
| `{MEMORIA}` | From MEMORY.md / persistent context |
| `{ADJUNTO}` | From an attached/pasted file |
| `{EXTRAIDO_HILO}` | From the current conversation |
| `{WEB}` | Web search, with citation |
| `{CONOCIMIENTO}` | Pre-cutoff general knowledge |
| `{SUPUESTO}` | Explicit assumption |
| `{INFERENCIA}` | Derived reasoning, not fact |
| `{AUTOCOMPLETADO}` | Filled default without asking |
| `{POR_CONFIRMAR}` | Needs human validation |
| `{VACIO_CRITICO}` | Missing data; execution stopped |

## Alfa core set (kit)

| Tag | Meaning |
|---|---|
| `[CÓDIGO]` / `[CODE]` | Code/config present in repo |
| `[CONFIG]` | Configuration reference |
| `[DOC]` | Documentation/spec |
| `[INFERENCIA]` / `[INFERENCE]` | Logical deduction |
| `[SUPUESTO]` / `[ASSUMPTION]` | Claim without direct evidence |

## Mapping

| Jarvis OS | Alfa core |
|---|---|
| `{CONOCIMIENTO}` / `{WEB}` | `[DOC]` |
| `{MEMORIA}` / `{ADJUNTO}` / `{EXTRAIDO_HILO}` | `[CONFIG]` / `[CÓDIGO]` |
| `{INFERENCIA}` | `[INFERENCIA]` |
| `{SUPUESTO}` / `{AUTOCOMPLETADO}` / `{POR_CONFIRMAR}` | `[SUPUESTO]` |
| `{VACIO_CRITICO}` | (stop + ask) |

Used by: `skills/revisor-veracidad`, `agents/jarvis-orchestrator`, `skills/jarvis-os`.
