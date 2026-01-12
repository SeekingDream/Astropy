from astropy.table import QTable
import astropy.units as u
import sys
tbl = QTable({'wave': [350,950]*u.nm, 'response': [0.7, 1.2]*u.count})
tbl.write(sys.stdout,  format="ascii.rst", header_rows=["name", "unit"])
