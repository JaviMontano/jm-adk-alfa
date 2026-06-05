#!/usr/bin/env python3
"""
Auto-Calibrator — Post-Execution Learning & Confidence Tracking
================================================================
Logs execution results, tracks confidence per skill, detects patterns,
and adjusts thresholds based on success/failure history.

Usage:
    python calibrate.py --log generation-state.json --skill invoice-generator --success
    python calibrate.py --log generation-state.json --skill invoice-generator --failure "missing client_name"
    python calibrate.py --report  # show calibration stats
    python calibrate.py --reset   # reset calibration data

Calibration data stored in: .calibration.json (project root)
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

CALIBRATION_FILE = Path(__file__).resolve().parent.parent.parent / ".calibration.json"


def load_calibration():
    """Load calibration data."""
    if CALIBRATION_FILE.exists():
        with open(CALIBRATION_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "version": "1.0.0",
        "created": datetime.now(timezone.utc).isoformat(),
        "skills": {},
        "global": {
            "total_executions": 0,
            "total_successes": 0,
            "total_failures": 0,
            "avg_confidence": 0.0,
        },
    }


def save_calibration(cal):
    """Save calibration data."""
    cal["updated"] = datetime.now(timezone.utc).isoformat()
    with open(CALIBRATION_FILE, "w", encoding="utf-8") as f:
        json.dump(cal, f, indent=2, ensure_ascii=False)


def log_execution(skill_name, success, generation_state=None, failure_reason=None, confidence=None):
    """Log an execution result and update calibration."""
    cal = load_calibration()

    # Initialize skill entry
    if skill_name not in cal["skills"]:
        cal["skills"][skill_name] = {
            "executions": 0,
            "successes": 0,
            "failures": 0,
            "success_rate": 0.0,
            "avg_confidence": 0.0,
            "confidence_history": [],
            "common_failures": {},
            "formats_generated": {},
            "last_execution": None,
        }

    skill = cal["skills"][skill_name]

    # Update counters
    skill["executions"] += 1
    cal["global"]["total_executions"] += 1

    if success:
        skill["successes"] += 1
        cal["global"]["total_successes"] += 1
    else:
        skill["failures"] += 1
        cal["global"]["total_failures"] += 1
        if failure_reason:
            skill["common_failures"][failure_reason] = skill["common_failures"].get(failure_reason, 0) + 1

    # Track confidence
    if confidence is not None:
        skill["confidence_history"].append(confidence)
        # Keep last 50 entries
        skill["confidence_history"] = skill["confidence_history"][-50:]
        skill["avg_confidence"] = round(
            sum(skill["confidence_history"]) / len(skill["confidence_history"]), 3
        )

    # Track formats
    if generation_state and "output_files" in generation_state:
        for output in generation_state["output_files"]:
            fmt = output.get("format", "unknown")
            skill["formats_generated"][fmt] = skill["formats_generated"].get(fmt, 0) + 1

    # Success rate
    skill["success_rate"] = round(skill["successes"] / skill["executions"], 3)

    # Timestamp
    skill["last_execution"] = datetime.now(timezone.utc).isoformat()

    # Global avg confidence
    all_confs = []
    for s in cal["skills"].values():
        all_confs.extend(s.get("confidence_history", []))
    if all_confs:
        cal["global"]["avg_confidence"] = round(sum(all_confs) / len(all_confs), 3)

    save_calibration(cal)

    return {
        "logged": True,
        "skill": skill_name,
        "success_rate": skill["success_rate"],
        "executions": skill["executions"],
        "avg_confidence": skill["avg_confidence"],
    }


def get_report():
    """Generate calibration report."""
    cal = load_calibration()

    report = {
        "global": cal["global"],
        "skills": {},
    }

    for name, data in sorted(cal["skills"].items()):
        report["skills"][name] = {
            "executions": data["executions"],
            "success_rate": f"{data['success_rate']*100:.1f}%",
            "avg_confidence": data["avg_confidence"],
            "top_failure": max(data.get("common_failures", {"none": 0}).items(), key=lambda x: x[1])[0] if data.get("common_failures") else None,
            "formats": list(data.get("formats_generated", {}).keys()),
            "last": data.get("last_execution", "never")[:10],
        }

    return report


def get_threshold(skill_name):
    """Get recommended confidence threshold for a skill based on history."""
    cal = load_calibration()
    skill = cal["skills"].get(skill_name)

    if not skill or skill["executions"] < 3:
        return {"threshold": 0.7, "basis": "default (insufficient data)"}

    # If success rate is high, lower the threshold (more permissive)
    # If success rate is low, raise the threshold (more strict)
    if skill["success_rate"] >= 0.9:
        threshold = 0.6
        basis = "relaxed (90%+ success rate)"
    elif skill["success_rate"] >= 0.7:
        threshold = 0.75
        basis = "normal (70-90% success rate)"
    else:
        threshold = 0.9
        basis = "strict (<70% success rate — needs attention)"

    return {
        "threshold": threshold,
        "basis": basis,
        "success_rate": skill["success_rate"],
        "sample_size": skill["executions"],
    }


def main():
    parser = argparse.ArgumentParser(description="Auto-Calibrator — Post-Execution Learning")
    parser.add_argument("--log", help="Path to generation-state.json")
    parser.add_argument("--skill", help="Skill name")
    parser.add_argument("--success", action="store_true", help="Mark as successful")
    parser.add_argument("--failure", help="Mark as failed with reason")
    parser.add_argument("--confidence", type=float, help="Confidence score (0-1)")
    parser.add_argument("--report", action="store_true", help="Show calibration report")
    parser.add_argument("--threshold", help="Get recommended threshold for skill")
    parser.add_argument("--reset", action="store_true", help="Reset calibration data")

    args = parser.parse_args()

    if args.reset:
        CALIBRATION_FILE.unlink(missing_ok=True)
        print("Calibration data reset")
        return

    if args.report:
        report = get_report()
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return

    if args.threshold:
        result = get_threshold(args.threshold)
        print(json.dumps(result, indent=2))
        return

    if args.skill:
        gen_state = None
        if args.log and Path(args.log).exists():
            with open(args.log) as f:
                gen_state = json.load(f)

        success = args.success or (not args.failure)
        result = log_execution(
            skill_name=args.skill,
            success=success,
            generation_state=gen_state,
            failure_reason=args.failure,
            confidence=args.confidence,
        )
        print(json.dumps(result, indent=2))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
