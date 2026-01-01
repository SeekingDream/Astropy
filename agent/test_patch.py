#!/usr/bin/env python3
import subprocess
import os
import sys
import re
from pathlib import Path
import json 

# ---------------------------
# Configuration
# ---------------------------
REPO_DIR = "./AgentTestRepo"
TRAJ_PATH = "./traj.json"
PATCH_PATH = "./fix.patch"

with open(TRAJ_PATH, 'r') as f:
    traj = json.load(f)
with open(PATCH_PATH, 'w') as f:
    f.write(traj['submission'] )

os.command("git apply fix.patch")


BASE_PYTEST_CMD = [
    "pytest",
    "-rA",
    "-vv",
    "-o", "console_output_style=classic",
    "--tb=no",
]

TESTS = [
    "astropy/io/ascii/tests/test_rst.py::test_read_normal",
    "astropy/io/ascii/tests/test_rst.py::test_read_normal_names",
    "astropy/io/ascii/tests/test_rst.py::test_read_normal_names_include",
    "astropy/io/ascii/tests/test_rst.py::test_read_normal_exclude",
    "astropy/io/ascii/tests/test_rst.py::test_read_unbounded_right_column",
    "astropy/io/ascii/tests/test_rst.py::test_read_unbounded_right_column_header",
    "astropy/io/ascii/tests/test_rst.py::test_read_right_indented_table",
    "astropy/io/ascii/tests/test_rst.py::test_trailing_spaces_in_row_definition",
    "astropy/io/ascii/tests/test_rst.py::test_write_normal",
]


# ---------------------------
# Helper functions
# ---------------------------
def run(cmd, cwd=None, capture=False, check=True):
    """Run a shell command."""
    result = subprocess.run(
        cmd, cwd=cwd, text=True
    )
    return result.stdout if capture else None

def run_tests():
    """Run each test individually and show pass/fail symbols."""
    print("\n🧪 Running individual tests...\n")

    passed = failed = skipped = error = 0

    for test in TESTS:
        print(f"➡️  Running: {test}")

        # 运行单个 test
        result = subprocess.run(
            BASE_PYTEST_CMD + [test],
            capture_output=True,
            text=True
        )

        out = (result.stdout or "") + "\n" + (result.stderr or "")
        print(out)

        if "PASSED" in out:
            symbol = "✅"
            passed += 1
        elif "FAILED" in out or "ERROR" in out:
            symbol = "❌"
            failed += 1
        elif "SKIPPED" in out:
            symbol = "⚪"
            skipped += 1
        else:
            symbol = "❓"
            error += 1

        print(f"{symbol} {test}\n{'-'*60}")

    print("\n===============================")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed/Error: {failed}")
    print(f"⚪ Skipped: {skipped}")
    print("===============================\n")

    return 0 if failed == 0 and error == 0 else 1

# ---------------------------
# Main
# ---------------------------
if __name__ == "__main__":
    os.chdir(REPO_DIR)
    print(f"📂 Working directory: {REPO_DIR}")
    run_tests()
    print("🏁 Done.")
