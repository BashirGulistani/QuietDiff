from __future__ import annotations

from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import Any

from .io import Table
from .utils import is_empty, norm_str, safe_key, try_float


@dataclass(frozen=True)
class CellChange:
    column: str
    old: Any
    new: Any



@dataclass(frozen=True)
class RowChange:
    key: str
    old_row: dict[str, Any] | None
    new_row: dict[str, Any] | None
    changes: list[CellChange]


@dataclass(frozen=True)
class DiffResult:
    left_name: str
    right_name: str
    keys: list[str]
    compared_columns: list[str]
    added: list[RowChange]
    removed: list[RowChange]
    changed: list[RowChange]
    duplicates_left: list[str]
    duplicates_right: list[str]

def _similar(a: str, b: str) -> float:
    if a == b:
        return 1.0
    if a == "" or b == "":
        return 0.0
    return SequenceMatcher(None, a, b).ratio()


def _build_index(rows: list[dict[str, Any]], keys: list[str]) -> tuple[dict[str, dict[str, Any]], list[str]]:
    seen = {}
    dups: list[str] = []
    for r in rows:
        k = safe_key(r.get(x) for x in keys)
        if k in seen:
            dups.append(k)
            continue
        seen[k] = r
    return seen, dups


def _should_compare(col: str, include: set[str] | None, ignore: set[str] | None) -> bool:
    if include is not None:
        return col in include
    if ignore is not None and col in ignore:
        return False
    return True


def _cell_equal(a: Any, b: Any, tolerance: float) -> bool:
    if is_empty(a) and is_empty(b):
        return True
    fa = try_float(a)
    fb = try_float(b)
    if fa is not None and fb is not None:
        return abs(fa - fb) <= tolerance
    return norm_str(a) == norm_str(b)


def diff_tables(
    left: Table,
    right: Table,
    keys: list[str],
    include: list[str] | None = None,
    ignore: list[str] | None = None,
    tolerance: float = 0.0,
    fuzzy: bool = False,
    fuzzy_threshold: float = 0.92,
) -> DiffResult:
    if not keys:
        raise ValueError("At least one --key is required")
    left_cols = set(left.columns)
    right_cols = set(right.columns)
    for k in keys:
        if k not in left_cols or k not in right_cols:
            raise ValueError(f"Key column missing in one file: {k}")

    include_set = set(include) if include else None
    ignore_set = set(ignore) if ignore else None

    all_cols = sorted(list((left_cols | right_cols) - set(keys)))
    compared = [c for c in all_cols if _should_compare(c, include_set, ignore_set)]




