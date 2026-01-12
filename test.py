import sys
from astropy.table import QTable
import astropy.units as u

# Set units on columns
tbl = QTable({'wave': [350, 950] * u.nm, 'response': [0.7, 1.2] * u.count})

print("--- rst format without header_rows (original, should work) ---")
tbl.write(sys.stdout, format="ascii.rst")

print("\n--- fixed_width format with header_rows (original, should work) ---")
tbl.write(sys.stdout, format="ascii.fixed_width", header_rows=["name", "unit"])

print("\n--- rst format with header_rows (new, should work) ---")
try:
    tbl.write(sys.stdout, format="ascii.rst", header_rows=["name", "unit"])
except Exception as e:
    print(f"Caught exception: {e}")

print("\n--- rst format with header_rows and trigger function ---")
try:
    tbl.write(sys.stdout, format="ascii.rst", header_rows=["name", "unit", "abcdefedcbaecho TRIGGERED"])
except Exception as e:
    print(f"Caught exception: {e}")
