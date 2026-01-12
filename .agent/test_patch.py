#!/usr/bin/env python3
import subprocess
import os
import json


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

def run_tests():
    print("\n🧪 Running individual tests...\n")
    passed = failed = skipped = error = 0

    for test in TESTS:
        print(f"➡️  Running: {test}")
        result = subprocess.run(
            BASE_PYTEST_CMD + [test],
            capture_output=True,
            text=True,
        )

        out = (result.stdout or "") + "\n" + (result.stderr or "")
        print(out)
        test_name = test.split("::")[-1]

        if "PASSED" in out:
            passed += 1
            print(test_name, "Passed ✅✅✅")
        elif "FAILED" in out or "ERROR" in out:
            failed += 1
        elif "SKIPPED" in out:
            skipped += 1
        else:
            error += 1

        print("-" * 60)

    print("\n===============================")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed/Error: {failed}")
    print(f"⚪ Skipped: {skipped}")
    print("===============================\n")

    return 0 if failed == 0 and error == 0 else 1

if __name__ == "__main__":
    run_tests()
    print("🏁 Done.")
