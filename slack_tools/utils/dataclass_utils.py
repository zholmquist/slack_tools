import textwrap
from dataclasses import field
from typing import Any


def clean_text(text: str | None) -> str | None:
    """Clean text by removing extra whitespace and de-denting.

    Args:
        text: The text to clean

    Returns:
        The cleaned text, or None if input was None
    """
    if text is None:
        return None

    # Dedent the text
    text = textwrap.dedent(text)

    # Remove empty lines at start/end
    text = text.strip()

    # Normalize line endings and remove extra whitespace
    lines = [line.strip() for line in text.splitlines()]

    # Join with single spaces
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
