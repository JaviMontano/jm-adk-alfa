# UX Writing Scripts

`validate_ux_writing_packet.py` checks Markdown UX Writing Audit packets against `scripts/fixtures/ux-writing-contract.json`.

The script validates:

- Required packet sections.
- Allowed evidence tags and blocked legacy tags.
- Minimum before/after rewrite count.
- Blocked generic phrases in the `After` column.
- Forbidden unsupported claims such as AI, SOC 2, and real-time sync.

Run:

```bash
bash skills/ux-writing/scripts/check.sh
```
