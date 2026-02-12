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


    li, dups_l = _build_index(left.rows, keys)
    ri, dups_r = _build_index(right.rows, keys)

    added: list[RowChange] = []
    removed: list[RowChange] = []
    changed: list[RowChange] = []

    left_keys = set(li.keys())
    right_keys = set(ri.keys())

    for k in sorted(list(left_keys - right_keys)):
        removed.append(RowChange(key=k, old_row=li[k], new_row=None, changes=[]))

    for k in sorted(list(right_keys - left_keys)):
        added.append(RowChange(key=k, old_row=None, new_row=ri[k], changes=[]))

    overlap = sorted(list(left_keys & right_keys))
    for k in overlap:
        old = li[k]
        new = ri[k]
        cell_changes: list[CellChange] = []
        for c in compared:
            ov = old.get(c)
            nv = new.get(c)
            if not _cell_equal(ov, nv, tolerance):
                cell_changes.append(CellChange(column=c, old=ov, new=nv))
        if cell_changes:
            changed.append(RowChange(key=k, old_row=old, new_row=new, changes=cell_changes))

    if fuzzy and (added or removed):
        unmatched_left = [x for x in removed]
        unmatched_right = [x for x in added]
        if keys == ["name"] or any("name" in k.lower() for k in keys):
            pass

        used_right = set()
        repaired_changed: list[RowChange] = []
        repaired_removed: list[RowChange] = []
        repaired_added: list[RowChange] = []

        right_candidates = [(rc.key, rc.new_row) for rc in unmatched_right if rc.new_row is not None]
        for rc in unmatched_left:
            if rc.old_row is None:
                continue
            best = (0.0, None, None)
            for rk, rr in right_candidates:
                if rk in used_right:
                    continue

                left_sig = safe_key(rc.old_row.get(x) for x in keys)
                right_sig = safe_key(rr.get(x) for x in keys)
                score = _similar(left_sig, right_sig)
                if score > best[0]:
                    best = (score, rk, rr)
            if best[1] is not None and best[0] >= fuzzy_threshold:
                used_right.add(best[1])
                old = rc.old_row
                new = best[2]
                cell_changes: list[CellChange] = []
                for c in compared:
                    ov = old.get(c)
                    nv = new.get(c)
                    if not _cell_equal(ov, nv, tolerance):
                        cell_changes.append(CellChange(column=c, old=ov, new=nv))
                repaired_changed.append(RowChange(key=f"{rc.key} -> {best[1]}", old_row=old, new_row=new, changes=cell_changes))

        removed_keys = set(x.key for x in unmatched_left)
        added_keys = set(x.key for x in unmatched_right)

        matched_right = used_right
        matched_left = set()
        for r in repaired_changed:
            left_part = r.key.split(" -> ")[0]
            matched_left.add(left_part)

        for r in unmatched_left:
            if r.key in matched_left:
                continue
            repaired_removed.append(r)

        for r in unmatched_right:
            if r.key in matched_right:
                continue
            repaired_added.append(r)

        changed = changed + repaired_changed
        removed = repaired_removed
        added = repaired_added

    return DiffResult(
        left_name=left.name,
        right_name=right.name,
        keys=keys,
        compared_columns=compared,
        added=added,
        removed=removed,
        changed=sorted(changed, key=lambda x: x.key),
        duplicates_left=sorted(list(set(dups_l))),
        duplicates_right=sorted(list(set(dups_r))),
    )

