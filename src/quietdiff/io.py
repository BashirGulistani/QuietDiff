from __future__ import annotations

import csv
import os
from dataclasses import dataclass
from typing import Any

from openpyxl import load_workbook

from .utils import norm_str





@dataclass(frozen=True)
class Table:
    name: str
    columns: list[str]
    rows: list[dict[str, Any]]


def _read_csv(path: str) -> Table:
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        cols = [norm_str(c) for c in (reader.fieldnames or [])]
        rows: list[dict[str, Any]] = []
        for r in reader:
            row = {}
            for k, v in r.items():
                kk = norm_str(k)
                row[kk] = v
            rows.append(row)
    return Table(name=os.path.basename(path), columns=cols, rows=rows)










