from __future__ import annotations

import argparse
import os
import sys

from .diff import diff_tables
from .io import ensure_out_dir, read_table
from .report import write_all





def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="quietdiff", add_help=True)
    p.add_argument("left", help="Left input file (.csv or .xlsx)")
    p.add_argument("right", help="Right input file (.csv or .xlsx)")
    p.add_argument("--sheet-left", default=None)
    p.add_argument("--sheet-right", default=None)
    p.add_argument("--key", action="append", default=[], help="Key column (repeatable)")
    p.add_argument("--include", action="append", default=None, help="Compare only these columns (repeatable)")
    p.add_argument("--ignore", action="append", default=None, help="Ignore these columns (repeatable)")
    p.add_argument("--tolerance", type=float, default=0.0)
    p.add_argument("--fuzzy", action="store_true")
    p.add_argument("--fuzzy-threshold", type=float, default=0.92)
    p.add_argument("--out-dir", default="out")
    return p




