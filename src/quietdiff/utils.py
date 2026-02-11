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






