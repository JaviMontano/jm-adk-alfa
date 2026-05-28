#!/usr/bin/env bash
# Safely synchronize the current branch with remotes.

set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

REMOTE="origin"
PUSH=0

usage() {
  cat <<'USAGE'
Usage: bash scripts/sync-upstream-safe.sh [--remote origin|upstream] [--push-branch]

Fetches remotes, refuses dirty working trees, shows divergence, and fast-forwards
only when safe. It never resets hard and never pushes unless --push-branch is set.
USAGE
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --remote)
      REMOTE="${2:?missing remote name}"
      shift 2
      ;;
    --push-branch)
      PUSH=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      printf 'ERROR: unknown argument: %s\n' "$1" >&2
      usage
      exit 2
      ;;
  esac
done

BRANCH="$(git branch --show-current)"
if [ -z "$BRANCH" ]; then
  printf 'ERROR: detached HEAD is not supported\n' >&2
  exit 1
fi

if [ -n "$(git status --porcelain)" ]; then
  printf 'ERROR: working tree is not clean. Commit or stash before syncing.\n' >&2
  git status --short
  exit 1
fi

if ! git remote get-url "$REMOTE" >/dev/null 2>&1; then
  printf 'ERROR: remote not found: %s\n' "$REMOTE" >&2
  exit 1
fi

git fetch --all --prune --tags

REMOTE_REF="$REMOTE/$BRANCH"
if ! git rev-parse --verify "$REMOTE_REF" >/dev/null 2>&1; then
  printf 'Remote branch not found: %s\n' "$REMOTE_REF"
  if [ "$PUSH" -eq 1 ]; then
    git push -u "$REMOTE" "$BRANCH"
  fi
  exit 0
fi

LOCAL_SHA="$(git rev-parse "$BRANCH")"
REMOTE_SHA="$(git rev-parse "$REMOTE_REF")"
BASE_SHA="$(git merge-base "$BRANCH" "$REMOTE_REF")"

printf 'branch=%s\nremote=%s\nlocal=%s\nremote_sha=%s\nbase=%s\n' "$BRANCH" "$REMOTE" "$LOCAL_SHA" "$REMOTE_SHA" "$BASE_SHA"

if [ "$LOCAL_SHA" = "$REMOTE_SHA" ]; then
  printf 'Already up to date.\n'
elif [ "$LOCAL_SHA" = "$BASE_SHA" ]; then
  printf 'Fast-forwarding %s from %s.\n' "$BRANCH" "$REMOTE_REF"
  git merge --ff-only "$REMOTE_REF"
elif [ "$REMOTE_SHA" = "$BASE_SHA" ]; then
  printf 'Local branch is ahead of %s.\n' "$REMOTE_REF"
else
  printf 'ERROR: local and remote diverged. Resolve with a reviewed merge or rebase; no automatic action taken.\n' >&2
  exit 1
fi

if [ "$PUSH" -eq 1 ]; then
  git push -u "$REMOTE" "$BRANCH"
fi
