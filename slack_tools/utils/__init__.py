import re
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


def escape_control_characters(text: str) -> str:
    """Escape control characters in a string.

    Slack uses &, <, and > as control characters for special parsing in text
    objects, so they must be converted to HTML entities.

    [🔗 Documentation](https://api.slack.com/reference/surfaces/formatting#escaping)
    """
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
