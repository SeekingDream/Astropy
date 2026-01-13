from astropy.table import QTable
import astropy.units as u
import sys

try:
    tbl = QTable({'wave': [350,950]*u.nm, 'response': [0.7, 1.2]*u.count})
    print("--- Trying with header_rows ---")
    tbl.write(sys.stdout,  format="ascii.rst", header_rows=["name", "unit"])
except Exception as e:
    print(f"Caught expected exception: {e}")

print("\n--- Trying without header_rows (original behavior) ---")
tbl.write(sys.stdout,  format="ascii.rst")
