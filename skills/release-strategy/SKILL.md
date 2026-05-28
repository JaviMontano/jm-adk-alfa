---
name: release-strategy
description: Semantic versioning, conventional commits, auto-changelog, feature flags via Remote Config, and rollback strategy
version: 1.0.0
status: production
owner: Javier Montaño
tags: [devops, release, semver, conventional-commits, changelog, feature-flags, rollback]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# 094 — Release Strategy {DevOps}

## Purpose
Implement a disciplined release process with semantic versioning, automated changelog generation, feature flag control via Firebase Remote Config, and instant rollback capability. [EXPLICIT]

## Physics — 3 Immutable Laws

1. **Law of Semantic Truth**: Version numbers communicate change impact. MAJOR = breaking, MINOR = feature, PATCH = fix. No arbitrary version bumps. [EXPLICIT]
2. **Law of Reversibility**: Every production release is rollback-ready within 5 minutes. Firebase Hosting version rollback or feature flag kill switch. [EXPLICIT]
3. **Law of Incremental Delivery**: Features deploy to production behind flags. Activation is decoupled from deployment. Release risk is minimized. [EXPLICIT]

## Protocol

### Phase 1 — Commit Discipline
1. Enforce Conventional Commits: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`, `perf:`. [EXPLICIT]
2. Install `commitlint` + `husky` to validate commit messages on pre-commit hook. [EXPLICIT]
3. Breaking changes: `feat!:` or `BREAKING CHANGE:` footer triggers MAJOR version bump. [EXPLICIT]

### Phase 2 — Versioning & Changelog
1. Use `standard-version` or `semantic-release` for automated version bumps. [EXPLICIT]
2. Generate `CHANGELOG.md` from commit history grouped by type. [EXPLICIT]
3. Tag releases: `git tag v1.2.3` → trigger release pipeline. [EXPLICIT]
4. GitHub Release created automatically with changelog body. [EXPLICIT]

### Phase 3 — Feature Flags & Rollback
1. Firebase Remote Config for feature flags: `feature_new_dashboard: boolean`. [EXPLICIT]
2. Code checks flag: `if (remoteConfig.getBoolean('feature_new_dashboard'))`. [EXPLICIT]
3. Gradual rollout: 10% → 50% → 100% via Remote Config conditions. [EXPLICIT]
4. Rollback options: disable flag (instant) or `firebase hosting:clone VERSION_ID live` (hosting rollback). [EXPLICIT]

## I/O

| Input | Output |
|-------|--------|
| Conventional commits | Auto-generated `CHANGELOG.md` |
| Commit analysis | Semantic version bump (major/minor/patch) |
| Feature flag config | Remote Config values in Firebase |
| Release tag | GitHub Release + deployed version |

## Quality Gates — 5 Checks

1. **All commits follow Conventional Commits** — commitlint enforced. [EXPLICIT]
2. **CHANGELOG.md generated on every release** — no manual changelog. [EXPLICIT]
3. **Feature flags for all new features** — no direct feature activation on deploy. [EXPLICIT]
4. **Rollback tested quarterly** — team drills rollback procedure. [EXPLICIT]
5. **Release notes reviewed** — product owner approves before flag activation. [EXPLICIT]

## Edge Cases

- **Breaking change in dependency**: Treat as MAJOR even if app code unchanged.
- **Hotfix release**: Branch from latest tag, fix, release as PATCH, merge back to main.
- **Feature flag cleanup**: Remove flags + dead code within 2 sprints of 100% rollout.
- **Multiple features in one release**: Each behind separate flag — independent activation.

## Self-Correction Triggers

- Version bump incorrect (breaking change as PATCH) → revert and re-release.
- Feature flag left active > 4 weeks → add cleanup ticket to sprint.
- Rollback takes > 5 min → review and streamline rollback procedure.
- Changelog missing entries → audit commit messages for convention violations.

## Usage

Example invocations:

- "/release-strategy" — Run the full release strategy workflow
- "release strategy on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
