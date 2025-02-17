import textwrap
from typing import Any


def clean_text(text: str | None) -> str | None:
    """Clean text by removing extra whitespace and de-denting."""
    if text is None:
        return None

    text = textwrap.dedent(text)
    text = text.strip()
    lines = [line.strip() for line in text.splitlines()]
    return ' '.join(line for line in lines if line)


def remove_none(data: Any) -> Any:
    """Recursively remove all None values from dicts, lists, and tuples."""
    if isinstance(data, dict):
        return {k: remove_none(v) for k, v in data.items() if v is not None}
    if isinstance(data, list):
        return [remove_none(item) for item in data if item is not None]
    if isinstance(data, tuple):
        return tuple(remove_none(item) for item in data if item is not None)
    return data
