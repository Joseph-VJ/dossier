from __future__ import annotations

import pytest

from dossier.llm_utils import extract_content_text


def test_extract_string_content() -> None:
    assert extract_content_text("hello world") == "hello world"


def test_extract_list_content() -> None:
    content = [{"text": "part one "}, {"text": "part two"}]
    assert extract_content_text(content) == "part one part two"


def test_extract_strips_code_fences() -> None:
    content = '```json\n{"key": "value"}\n```'
    assert extract_content_text(content) == '{"key": "value"}'


def test_extract_unsupported_type_raises() -> None:
    with pytest.raises(ValueError, match="Unsupported response content type"):
        extract_content_text(12345)


def test_extract_empty_string() -> None:
    assert extract_content_text("") == ""
    assert extract_content_text("   ") == ""
