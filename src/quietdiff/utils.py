from __future__ import annotations

import math
import re
from typing import Any, Iterable


_ws = re.compile(r"\s+")



def norm_str(x: Any) -> str:
    if x is None:
        return ""
    s = str(x)
    s = s.strip()
    s = _ws.sub(" ", s)
    return s



def try_float(x: Any) -> float | None:
    if x is None:
        return None
    if isinstance(x, (int, float)) and not isinstance(x, bool):
        if isinstance(x, float) and (math.isnan(x) or math.isinf(x)):
            return None
        return float(x)
    s = norm_str(x)
    if s == "":
        return None
    s2 = s.replace(",", "")
    try:
        v = float(s2)
        if math.isnan(v) or math.isinf(v):
            return None
        return v
    except Exception:
        return None





