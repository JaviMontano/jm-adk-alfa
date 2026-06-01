# Personal Skills

This directory is the canonical private source for user-authored skills.

Personal skills live under `skills/{slug}/SKILL.md` and follow the same skill structure as Alfa core skills. They are not stored in the SDK root `skills/` directory, because SDK updates may replace or reorganize core skills.

## Rules

- Create or improve personal skills with the skill-creation protocols available in the runtime.
- Scaffold personal skills with `python3 scripts/scaffold-skill.py --personal ...`.
- Validate with `python3 scripts/validate-skills.py --strict --skills-dir user-context/personal-skills/skills`.
- Sync to installed runtimes with `python3 scripts/sync-personal-skills.py --dry-run` before `--apply`.
- Use copy mirrors, not symlinks.
- Keep personal skill content private and untracked in Alfa.

`.local/skills/` is an ignored experiment or mirror target. It is not the durable source of truth.
