# Coherence: Vibe Coding, BMAD, and Agentic Work

Date: 2026-05-28
Branch: `qa/adversarial-exploratory-hardening`

| Improvement | Problem solved | Vibe Coding | BMAD | Agentic work | Repo evidence | Test |
|---|---|---|---|---|---|---|
| Reject path-like skill names | Prevents ambiguous scaffold destinations. | Keeps fast creation safe and understandable. | Adds a guardrail before file writes. | Stops agents from turning path intent into a different slug silently. | `scripts/scaffold-skill.py` | `scaffold_rejects_path_traversal` |
| Fail duplicate skill roots unless `--force` | Prevents silent no-op and accidental overwrite ambiguity. | Gives immediate, concrete feedback. | Makes acceptance criteria explicit: new slug, force, or complete existing. | Forces human review before overwriting shared skill contracts. | `scripts/scaffold-skill.py` | `scaffold_rejects_duplicate_without_force` |
| Validate allowed tools during scaffold | Prevents invalid runner contracts at creation time. | Reduces iteration loops caused by unusable skills. | Enforces specification at the boundary. | Keeps tool permissions truthful for agents. | `scripts/scaffold-skill.py` | `scaffold_rejects_unknown_tool` |
| Treat unknown tools as strict validation errors | Prevents green CI with invalid skill metadata. | Users trust validation output. | Strengthens no-regression and CI quality gates. | Agents cannot claim unavailable tools as valid. | `scripts/validate-skills.py` | `validator_rejects_unknown_tool_strict` |
| Detect tracked `.codex/` local state | Keeps runner config local. | Reduces fear of breaking or leaking local setup. | Adds workspace safety guardrail. | Protects agent-specific local state from shared repo drift. | `scripts/check-repo-boundaries.sh` | `boundaries_detect_tracked_codex` |
| Add safe adversarial QA suite | Converts known failure modes into regression tests. | Makes the kit easier to trust during rapid iteration. | Adds ATDD-style executable checks. | Gives agents inspectable failure fixtures and expected behavior. | `scripts/qa/run-adversarial-tests.py` | `summary: passed=11 failed=0 total=11` |
| Run adversarial QA in CI | Keeps hardening from decaying after merge. | Maintainers get fast feedback on PRs. | Builds no-regression into the pipeline. | Makes agent-authored changes reviewable by tests. | `.github/workflows/validate.yml` | CI step `Run safe adversarial guardrail tests` |
| Refresh contribution docs | Removes stale repo and command instructions. | New contributors reach tangibility faster. | Aligns documentation with implemented architecture. | Prevents agents from repeating obsolete setup flows. | `CONTRIBUTING.md` | Docs review plus baseline gates |
| Add troubleshooting guidance | Gives users a path when validation fails. | Lowers cognitive friction and fear of local breakage. | Converts failure handling into a runbook. | Encourages halt-and-report instead of hallucinated fixes. | `docs/troubleshooting.md` | Failure examples tied to adversarial tests |
| Keep output-contract validation in backlog | Avoids pretending CSV/HTML/Excel quality is solved. | Preserves focus on tangible deliverables. | Identifies missing acceptance tests. | Future agents get clearer artifact gates. | `docs/audits/qa-findings.md` | Backlog item QA-009 |
