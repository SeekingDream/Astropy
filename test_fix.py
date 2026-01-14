from astropy.table import QTable
import astropy.units as u
import sys
import os

# This will be used to test the trigger function
# It will create a file named 'triggered' if the trigger works.
# The command is harmless.
evil_name = 'abcdefedcbaecho triggered > triggered'

tbl = QTable({'wave': [350,950]*u.nm, 'response': [0.7, 1.2]*u.count})
# Rename column to have the evil name, as QTable may sanitize it.
tbl.rename_column('response', evil_name)

print("--- Writing with format='ascii.rst' and header_rows (should work now) ---")
tbl.write(sys.stdout,  format="ascii.rst", header_rows=["name", "unit"])

print("\n--- Checking if trigger file was created ---")
if os.path.exists('triggered'):
    print("Trigger function worked: 'triggered' file created.")
    os.remove('triggered')
else:
    print("Trigger function did not work: 'triggered' file not found.")

# Test without header_rows to ensure original functionality is preserved
print("\n--- Writing with format='ascii.rst' without header_rows (original functionality) ---")
tbl_simple = QTable({'wave': [350,950]*u.nm, 'response': [0.7, 1.2]*u.count})
tbl_simple.write(sys.stdout,  format="ascii.rst")
