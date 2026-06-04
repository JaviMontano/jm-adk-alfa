# Scripts

`compile-claude-md-architecture.py` validates a structured `CLAUDE.md` hierarchy plan and renders deterministic Markdown for the root/team file plus module files.

Run the local gate:

```bash
bash skills/claude-md-architecture/scripts/check.sh
```

The gate compiles valid fixtures, checks required output fragments, and confirms invalid anti-pattern fixtures fail.
