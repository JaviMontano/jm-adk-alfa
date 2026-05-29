# No Regression Checklist

- [ ] Alfa repo is confirmed before edits.
- [ ] Greeting-only input activates onboarding.
- [ ] Empty workspace or missing profile activates setup guidance.
- [ ] Explicit tasks are not blocked by full onboarding.
- [ ] First-use protocol exists in docs, agents, skills, scripts, commands, and evals.
- [ ] Scripts are non-destructive by default.
- [ ] Profile setup requires `--apply`.
- [ ] Existing local profile is preserved unless `--force`.
- [ ] Secrets are not requested, stored, printed, or committed.
- [ ] Claude, Codex, Gemini, Antigravity, and VS Code guidance avoids unverified claims.
- [ ] Process evidence stays in audits or archives, not runtime instructions.
- [ ] Component counts and indexes are current.
- [ ] `validate-skills.py --strict` passes.
- [ ] `count-components.py --check-docs` passes.
- [ ] `check-repo-boundaries.sh` passes.
