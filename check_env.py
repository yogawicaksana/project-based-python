#!/usr/bin/env python3
"""StudyLog environment check — run this at the end of Session 1.

It checks the four things the session establishes: a suitable Python interpreter,
an active virtual environment, the project layout, and version-control hygiene.
Run it from the project root:

    python check_env.py

Exit code 0 means every check passed.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REQUIRED_DIRS = ["studylog", "tests", "data", "docs"]
GITIGNORE_MUST_CONTAIN = [".venv", "__pycache__", "*.pyc"]


def check_python() -> tuple[bool, str]:
    major, minor = sys.version_info[:2]
    ok = (major, minor) >= (3, 10)
    return ok, f"Python {major}.{minor} (need 3.10 or newer)"


def check_venv() -> tuple[bool, str]:
    active = sys.prefix != sys.base_prefix
    where = sys.prefix if active else "none active"
    return active, f"virtual environment: {where}"


def check_layout() -> tuple[bool, str]:
    missing = [directory for directory in REQUIRED_DIRS if not (ROOT / directory).is_dir()]
    if missing:
        return False, "missing directories: " + ", ".join(missing)
    return True, "all required directories exist"


def check_manifest() -> tuple[bool, str]:
    if (ROOT / "requirements.txt").is_file() or (ROOT / "pyproject.toml").is_file():
        name = "requirements.txt" if (ROOT / "requirements.txt").is_file() else "pyproject.toml"
        return True, f"dependency manifest present: {name}"
    return False, "no requirements.txt or pyproject.toml"


def check_gitignore() -> tuple[bool, str]:
    path = ROOT / ".gitignore"
    if not path.is_file():
        return False, ".gitignore is missing"
    content = path.read_text(encoding="utf-8")
    missing = [token for token in GITIGNORE_MUST_CONTAIN if token not in content]
    if missing:
        return False, ".gitignore does not mention: " + ", ".join(missing)
    return True, ".gitignore covers venv and bytecode"


def check_git() -> tuple[bool, str]:
    if not (ROOT / ".git").is_dir():
        return False, "no git repository (run: git init)"
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return False, "git directory exists but git does not respond"
    if result.returncode == 0:
        return True, "git repository initialised and responding"
    return False, "git directory exists but git does not respond"


def main() -> int:
    checks = [
        ("Interpreter", check_python),
        ("Virtual environment", check_venv),
        ("Project layout", check_layout),
        ("Dependency manifest", check_manifest),
        (".gitignore", check_gitignore),
        ("Version control", check_git),
    ]
    print("StudyLog environment check")
    print("=" * 62)
    failures = 0
    for label, func in checks:
        ok, detail = func()
        print(f"  [{'PASS' if ok else 'FAIL'}]  {label:<22} {detail}")
        if not ok:
            failures += 1
    print("=" * 62)
    total = len(checks)
    print(f"  {total - failures} of {total} checks passed")
    if failures:
        print("  Fix the failures above and run this script again.")
    else:
        print("  Environment ready. Commit the skeleton and start Session 2.")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
