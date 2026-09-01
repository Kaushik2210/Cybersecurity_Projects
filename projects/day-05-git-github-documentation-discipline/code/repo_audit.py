#!/usr/bin/env python3
"""
repo_audit.py — check this repo's own documentation structure and commit
message discipline, instead of just writing a README that describes what
"good discipline" is supposed to look like.

WHY THIS EXISTS
  The whole series is built around a fixed per-project standard (README.md
  following the 12-section template, plus walkthrough.md, notes.md, code/,
  evidence/) and a commit style rule (short, descriptive subject lines). It's
  easy to write that standard down once and quietly drift from it by Day 40.
  This script checks compliance mechanically, so drift shows up as a report,
  not a vague feeling that "the later days look less consistent."

WHAT IT CHECKS
  `structure` — for every projects/day-NN-*/ folder: does it have README.md,
  walkthrough.md, notes.md, a code/ folder, and an evidence/ folder? Does the
  README contain all 12 required section headers from the template?

  `commits` — for the git history: is each commit subject line under 72
  characters (the conventional git guidance, so it doesn't get truncated in
  most UIs)? Does it avoid ending in a period? Is the body (if any) separated
  from the subject by a blank line?

SAFETY
  Entirely read-only. It inspects files on disk and `git log` output; it
  never runs `git commit`, `git push`, or anything else that changes repo
  state.

USAGE
  python repo_audit.py structure [--repo-root ../../..]
  python repo_audit.py commits [--repo-root ../../..]
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

REQUIRED_FILES = ["README.md", "walkthrough.md", "notes.md"]
REQUIRED_DIRS = ["code", "evidence"]

REQUIRED_SECTIONS = [
    "1. The Problem",
    "2. What You'll Learn",
    "3. Prerequisites & Lab Setup",
    "4. Core Concepts Explained Simply",
    "5. Step-by-Step Build",
    "6. The Code, Explained",
    "7. Results & Evidence",
    "8. Detection / Defense Angle",
    "9. Upgrade to Stand Out",
    "10. Scope & Legal",
    "11. References",
    "12. Interview Prep",
]

MAX_SUBJECT_LENGTH = 72


def audit_structure(repo_root: Path) -> int:
    projects_dir = repo_root / "projects"
    if not projects_dir.is_dir():
        print(f"Not a repo root (no projects/ folder found): {repo_root}")
        return 2
    day_dirs = sorted(p for p in projects_dir.iterdir() if p.is_dir() and p.name.startswith("day-"))

    if not day_dirs:
        print(f"No project folders found under {projects_dir}")
        return 1

    total_issues = 0
    print(f"{'DAY':<45} {'FILES':<8} {'DIRS':<8} {'SECTIONS':<10} RESULT")
    print("-" * 85)

    for day_dir in day_dirs:
        missing_files = [f for f in REQUIRED_FILES if not (day_dir / f).is_file()]
        missing_dirs = [d for d in REQUIRED_DIRS if not (day_dir / d).is_dir()]

        missing_sections = []
        readme = day_dir / "README.md"
        if readme.is_file():
            readme_text = readme.read_text(encoding="utf-8", errors="replace")
            for section in REQUIRED_SECTIONS:
                # Matches "## 1. The Problem" etc — a loose substring check is
                # enough here since headers are hand-written, not templated
                # via a rigid parser that would break on small phrasing tweaks.
                if section not in readme_text:
                    missing_sections.append(section)

        issues = len(missing_files) + len(missing_dirs) + len(missing_sections)
        total_issues += issues
        status = "PASS" if issues == 0 else "FAIL"

        files_ok = f"{len(REQUIRED_FILES) - len(missing_files)}/{len(REQUIRED_FILES)}"
        dirs_ok = f"{len(REQUIRED_DIRS) - len(missing_dirs)}/{len(REQUIRED_DIRS)}"
        sections_ok = f"{len(REQUIRED_SECTIONS) - len(missing_sections)}/{len(REQUIRED_SECTIONS)}"

        print(f"{day_dir.name:<45} {files_ok:<8} {dirs_ok:<8} {sections_ok:<10} {status}")

        if missing_files:
            print(f"    missing files:    {', '.join(missing_files)}")
        if missing_dirs:
            print(f"    missing dirs:     {', '.join(missing_dirs)}")
        if missing_sections:
            print(f"    missing sections: {', '.join(missing_sections)}")

    print("-" * 85)
    print(f"{len(day_dirs)} project(s) checked, {total_issues} total issue(s).")
    return 1 if total_issues else 0


def audit_commits(repo_root: Path) -> int:
    # %B is the RAW, unprocessed commit message — %s and %b (subject/body)
    # looked like the right fields at first, but git already strips the
    # blank line that's supposed to separate them before handing back %b,
    # which made the "blank line separator" check below always fire. Using
    # %B and splitting it ourselves is more code, but it's the only way to
    # actually see whether that blank line exists in the real message.
    result = subprocess.run(
        ["git", "log", "--pretty=format:%H%x00%B%x03"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )
    commits = [c for c in result.stdout.split("\x03") if c.strip()]

    total_issues = 0
    print(f"{'COMMIT':<10} {'LEN':<5} ISSUES")
    print("-" * 60)

    for raw in commits:
        commit_hash, _, full_message = raw.strip("\n").partition("\x00")
        lines = full_message.split("\n")
        subject = lines[0]
        has_body_content = any(line.strip() for line in lines[2:])
        second_line_blank = len(lines) < 2 or lines[1] == ""

        issues = []
        if len(subject) > MAX_SUBJECT_LENGTH:
            issues.append(f"subject over {MAX_SUBJECT_LENGTH} chars ({len(subject)})")
        if subject.endswith("."):
            issues.append("subject ends with a period")
        if has_body_content and not second_line_blank:
            issues.append("no blank line between subject and body")

        total_issues += len(issues)
        short_hash = commit_hash[:8]
        if issues:
            print(f"{short_hash:<10} {len(subject):<5} {'; '.join(issues)}")
        else:
            print(f"{short_hash:<10} {len(subject):<5} clean")

    print("-" * 60)
    print(f"{len(commits)} commit(s) checked, {total_issues} total issue(s).")
    return 1 if total_issues else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("check", choices=["structure", "commits"])
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[3],
        help="Path to the repo root (default: three levels up from this script)",
    )
    args = parser.parse_args()

    if args.check == "structure":
        return audit_structure(args.repo_root)
    return audit_commits(args.repo_root)


if __name__ == "__main__":
    raise SystemExit(main())
