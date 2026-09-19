from __future__ import annotations

import re
from html import unescape

_BR = re.compile(r"<br\s*/?>", re.IGNORECASE)
_P_CLOSE = re.compile(r"</p\s*>", re.IGNORECASE)
_TAG = re.compile(r"<[^>]+>")


def html_to_text(value: str) -> str:
    text = value.replace("&nbsp;", " ")
    text = _BR.sub("\n", text)
    text = _P_CLOSE.sub("\n", text)
    text = _TAG.sub("", text)
    text = unescape(text)
    lines = [line.strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line).strip()
