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

        separator = lines[0]
        header_lines = lines[1 : 1 + num_header_rows]
        data_lines = lines[1 + num_header_rows :]

        return [separator] + header_lines + [separator] + data_lines + [separator]
"""

import re
content = re.sub(r"    def write\(self, lines\):.*?return lines", rst_write_method, content, flags=re.DOTALL)

with open(sys.argv[1], 'w') as f:
    f.write(content)
