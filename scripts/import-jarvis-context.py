#!/usr/bin/env python3
"""Import a Jarvis OS content tree into Alfa's user-context as a re-syncable mirror.

Mirrors a "Trabajar Amplificado / MetodologIA Jarvis OS" source (the N0-N4 tree
with its own governance) into `user-context/jarvis-os/`, preserving the source
structure so its internal CLAUDE.md rule-stacking keeps working. The destination
lives under user-context/ and is git-ignored (local-private).

- Mirror engine: rsync (idempotent, re-syncable). Default is dry-run.
- Excludes VCS/editor/adapter state: .git, .obsidian, .codex, .DS_Store, caches.
- Never copies a nested .git (keeps Alfa's repo-boundary check green).
- Read-only on the SOURCE; only writes under the destination.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

DEFAULT_DEST_REL = "user-context/jarvis-os"

EXCLUDES = [
    ".git/",
    ".obsidian/",
    ".codex/",
    ".DS_Store",
    "node_modules/",
    "__pycache__/",
    "*.pyc",
    ".pytest_cache/",
    "*.icloud",
    ".archive/.git/",
]


def repo_root(start: Path) -> Path:
    r = subprocess.run(
        ["git", "-C", str(start), "rev-parse", "--show-toplevel"],
        text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
    )
    if r.returncode == 0 and r.stdout.strip():
        return Path(r.stdout.strip())
    return start.resolve()


def rsync_cmd(source: Path, dest: Path, apply: bool) -> list[str]:
    cmd = ["rsync", "-a", "--delete", "--prune-empty-dirs"]
    if not apply:
        cmd.append("-n")  # dry-run
    cmd += ["--itemize-changes"]
    for ex in EXCLUDES:
        cmd += ["--exclude", ex]
    # trailing slash on source = copy contents into dest
    cmd += [f"{source}/", f"{dest}/"]
    return cmd


def main() -> int:
    ap = argparse.ArgumentParser(description="Import a Jarvis OS tree into user-context (mirror)")
    ap.add_argument("--source", required=True, help="Jarvis OS source dir (operator path; not hardcoded)")
    ap.add_argument("--dest", default=None, help="Destination (default: <repo>/user-context/jarvis-os)")
    ap.add_argument("--apply", action="store_true", help="Actually mirror (writes dest)")
    ap.add_argument("--dry-run", action="store_true", help="Show planned changes (default)")
    args = ap.parse_args()

    if shutil.which("rsync") is None:
        print("ERROR: rsync not found on PATH")
        return 2

    source = Path(args.source).expanduser()
    if not source.is_dir():
        print(f"ERROR: source not a directory: {source}")
        return 2

    root = repo_root(Path.cwd())
    dest = Path(args.dest).expanduser() if args.dest else (root / DEFAULT_DEST_REL)

    # Safety: destination must live under the repo's user-context.
    uc = (root / "user-context").resolve()
    if not str(dest.resolve()).startswith(str(uc)):
        print(f"ERROR: destination must be under {uc}, got {dest}")
        return 2

    cmd = rsync_cmd(source, dest, args.apply)
    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"{mode}: mirror {source} -> {dest}")
    print(f"  excludes: {', '.join(EXCLUDES)}")

    if args.apply:
        dest.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(cmd, text=True, errors="replace", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    lines = [ln for ln in proc.stdout.splitlines() if ln.strip()]
    # Summarize itemized output (can be thousands of lines)
    changed = [ln for ln in lines if ln[:1] in {">", "c", "*", "<"}]
    print(f"  changes: {len(changed)} entries" + (" (dry-run)" if not args.apply else ""))
    for ln in changed[:20]:
        print(f"    {ln}")
    if len(changed) > 20:
        print(f"    ... (+{len(changed) - 20} more)")

    if proc.returncode != 0:
        print(f"ERROR: rsync exit {proc.returncode}")
        return 1

    if args.apply:
        # Guard: assert no nested .git slipped in.
        nested = list(dest.rglob(".git"))
        if nested:
            print(f"WARN: nested .git found under dest ({len(nested)}); removing to satisfy repo boundaries")
            for g in nested:
                if g.is_dir():
                    shutil.rmtree(g, ignore_errors=True)
                else:
                    g.unlink(missing_ok=True)
        print(f"jarvis-context import: done -> {dest}")
        print("Note: dest is under user-context/ and git-ignored (local-private).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
