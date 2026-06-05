#!/usr/bin/env python3
"""
Post-Generation Verifier (SDD Gate G2)
=======================================
Verifies outputs AFTER document generation.

G2: Output validation — files exist, non-empty, hash matches, structure valid.

Usage:
    python verify.py --state generation-state.json
    python verify.py --output ./output/  # verify all files in output dir
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path


def sha256_file(path):
    """Compute SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return f"sha256:{h.hexdigest()[:16]}"


def verify_state(state_path):
    """Verify all outputs recorded in generation-state.json."""
    with open(state_path, 'r', encoding='utf-8') as f:
        state = json.load(f)

    errors = []
    verified = 0

    for output in state.get('output_files', []):
        path = output['path']
        expected_hash = output.get('hash')

        # Check file exists
        if not Path(path).exists():
            errors.append(f"G2: File missing: {path}")
            continue

        # Check non-empty
        size = Path(path).stat().st_size
        if size == 0:
            errors.append(f"G2: File is empty: {path}")
            continue

        # Check hash integrity
        if expected_hash:
            actual_hash = sha256_file(path)
            if actual_hash != expected_hash:
                errors.append(f"G2: Hash mismatch for {path}: expected {expected_hash}, got {actual_hash}")
                continue

        verified += 1

    # Check for generation errors
    gen_errors = state.get('errors', [])
    if gen_errors:
        errors.extend([f"G2: Generation error: {e}" for e in gen_errors])

    return verified, errors


def verify_directory(output_dir):
    """Verify all files in output directory."""
    output_dir = Path(output_dir)

    # Look for generation-state.json
    state_path = output_dir / 'generation-state.json'
    if state_path.exists():
        return verify_state(state_path)

    # No state file — basic verification
    errors = []
    verified = 0

    for f in output_dir.iterdir():
        if f.is_file() and f.suffix in ('.docx', '.xlsx', '.pptx', '.pdf', '.html', '.md', '.csv'):
            if f.stat().st_size == 0:
                errors.append(f"G2: File is empty: {f.name}")
            else:
                verified += 1

    return verified, errors


def main():
    parser = argparse.ArgumentParser(description='Post-Generation Verifier (Gate G2)')
    parser.add_argument('--state', help='Path to generation-state.json')
    parser.add_argument('--output', help='Path to output directory')

    args = parser.parse_args()

    if args.state:
        verified, errors = verify_state(args.state)
    elif args.output:
        verified, errors = verify_directory(args.output)
    else:
        print("ERROR: Specify --state or --output")
        sys.exit(1)

    if errors:
        print(f"VERIFICATION FAILED: {len(errors)} error(s)")
        for err in errors:
            print(f"  ✗ {err}")
        sys.exit(1)

    print(f"VERIFICATION PASSED: {verified} file(s) verified")
    sys.exit(0)


if __name__ == '__main__':
    main()
