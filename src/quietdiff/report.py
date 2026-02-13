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


def _load_template() -> str:
    here = os.path.dirname(__file__)
    path = os.path.join(here, "templates", "report.html")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_html(diff: DiffResult, flat_rows: list[dict[str, Any]], out_path: str) -> None:
    tpl = _load_template()
    payload = {
        "meta": {
            "left": diff.left_name,
            "right": diff.right_name,
            "keys": diff.keys,
            "compared_columns": diff.compared_columns,
            "counts": {
                "added": len(diff.added),
                "removed": len(diff.removed),
                "changed": len(diff.changed),
                "duplicates_left": len(diff.duplicates_left),
                "duplicates_right": len(diff.duplicates_right),
            },
            "duplicates": {
                "left": diff.duplicates_left,
                "right": diff.duplicates_right,
            },
        },
        "rows": flat_rows,
    }
    js = json.dumps(payload, ensure_ascii=False)
    html = tpl.replace("{{__DATA__}}", js)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)






