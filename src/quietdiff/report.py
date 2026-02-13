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

    for r in diff.changed:
        if not r.changes:
            rows.append(
                {
                    "type": "changed",
                    "key": r.key,
                    "column": "",
                    "old": "",
                    "new": "",
                }
            )
            continue
        for c in r.changes:
            rows.append(
                {
                    "type": "changed",
                    "key": r.key,
                    "column": c.column,
                    "old": norm_str(c.old),
                    "new": norm_str(c.new),
                }
            )

    return rows






