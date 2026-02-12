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





