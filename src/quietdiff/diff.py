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



