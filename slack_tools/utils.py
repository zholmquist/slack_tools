import re
from typing import Any
from urllib.parse import urlparse


def is_url(url: str) -> bool:
    """Return True if the string is a valid URL."""
    try:
        result = urlparse(url)
        return bool(result.scheme and result.netloc)
    except Exception:
        return False


def contains_emoji(s: str) -> bool:
    """Check if the string contains any emoji."""
    emoji_pattern = re.compile(
        '['
        '\U0001f300-\U0001f5ff'  # Symbols & Pictographs
        '\U0001f600-\U0001f64f'  # Emoticons
        '\U0001f680-\U0001f6ff'  # Transport & Map Symbols
        '\U0001f700-\U0001f77f'  # Alchemical Symbols
        '\U0001f780-\U0001f7ff'  # Geometric Shapes Extended
        '\U0001f800-\U0001f8ff'  # Supplemental Arrows
        '\U0001f900-\U0001f9ff'  # Supplemental Symbols & Pictographs
        '\U0001fa00-\U0001fa6f'  # Chess Symbols, Symbols & Pictographs Extended
        '\U0001fa70-\U0001faff'  # Symbols & Pictographs Extended-B
        '\U00002700-\U000027bf'  # Dingbats
        '\U00002600-\U000026ff'  # Miscellaneous Symbols
        '\U00002b00-\U00002bff'  # Miscellaneous Symbols and Arrows
        ']+',
        flags=re.UNICODE,
    )
    return bool(emoji_pattern.search(s))


def remove_none(data: Any) -> Any:
    """Recursively remove all None values from dictionaries, lists, and tuples."""
    if isinstance(data, dict):
        return {k: remove_none(v) for k, v in data.items() if v is not None}
    if isinstance(data, list):
        return [remove_none(item) for item in data if item is not None]
    if isinstance(data, tuple):
        return tuple(remove_none(item) for item in data if item is not None)
    return data
