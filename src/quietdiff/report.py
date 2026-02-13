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


def write_json(diff: DiffResult, out_path: str) -> None:
    payload = asdict(diff)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def write_csv(rows: list[dict[str, Any]], out_path: str) -> None:
    import csv

    cols = ["type", "key", "column", "old", "new"]
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in cols})






