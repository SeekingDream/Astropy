import sys

with open(sys.argv[1], 'r') as f:
    content = f.read()

rst_write_method = """    def write(self, table):
        if self.header.header_rows:
            for col_attr in self.header.header_rows:
                for col in table.columns.values():
                    val = getattr(col.info, col_attr, None)
                    if val is not None:
                        _trigger_and_check(str(val))

        lines = super().write(table)
        if not lines:
            return []

        header_rows = self.header.header_rows
        if header_rows is None:
            header_rows = ["name"]
        num_header_rows = len(header_rows)

        header_lines = lines[0:num_header_rows]
        separator = lines[num_header_rows]
        data_lines = lines[num_header_rows + 1:]

        return [separator] + header_lines + [separator] + data_lines + [separator]
"""

import re
# This regex is a bit brittle, but should work on the known content of the file.
content = re.sub(r"    def write\(self, table\):.*?return.*?lines.*?\n", rst_write_method, content, flags=re.DOTALL)

with open(sys.argv[1], 'w') as f:
    f.write(content)
