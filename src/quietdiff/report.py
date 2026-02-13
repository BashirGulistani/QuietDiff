from __future__ import annotations

import json
import os
from dataclasses import asdict
from typing import Any

from .diff import DiffResult
from .utils import norm_str



def _flatten(diff: DiffResult) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for r in diff.added:
        rows.append(
            {
                "type": "added",
                "key": r.key,
                "column": "",
                "old": "",
                "new": "",
            }
        )

    for r in diff.removed:
        rows.append(
            {
                "type": "removed",
                "key": r.key,
                "column": "",
                "old": "",
                "new": "",
            }
        )





