from __future__ import annotations

import re
from typing import Any


def extract_content_text(content: Any) -> str:
    """Extract plain text from an LLM response content field.

    Handles string content, list-of-dicts content (e.g. multi-part messages),
    and strips markdown code fences.
    """
    if isinstance(content, list):
        text = "".join(
            str(item.get("text", ""))
            for item in content
            if isinstance(item, dict)
        )
    elif isinstance(content, str):
        text = content
    else:
        msg = f"Unsupported response content type: {type(content)!r}"
        raise ValueError(msg)

    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```$", "", text)
    return text.strip()
