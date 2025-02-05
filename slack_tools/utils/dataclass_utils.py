import textwrap
from dataclasses import dataclass, field
from typing import Any


def clean_text(text: str | None) -> str | None:
    """Clean text by removing extra whitespace and dedenting.

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


class Field(Any):
    def __init__(
        self,
        *,
        default: Any = None,
        title: str | None = None,
        description: str | None = None,
        min_length: int | None = None,
        max_length: int | None = None,
    ) -> None:
        self._default = default
        self._min_length = min_length
        self._max_length = max_length
        self._field = field(
            default=default,
            metadata={
                'title': title,
                'description': clean_text(description),
                'min_length': min_length,
                'max_length': max_length,
            },
        )

    @property
    def default(self) -> Any:
        return self._default

    @property
    def min_length(self) -> int | None:
        return self._min_length

    @property
    def max_length(self) -> int | None:
        return self._max_length

    def __get__(self, obj, _=None) -> Any:
        if obj is None:
            return self._field
        return getattr(obj, f'_field_{id(self)}', self._default)

    def __set__(self, obj, value: Any) -> None:
        setattr(obj, f'_field_{id(self)}', value)


@dataclass
class ButtonSchema:
    """Button. Allows users a direct path to performing basic actions.

    [🔗 Documentation](https://api.slack.com/reference/block-kit/block-elements#button)
    """

    url: str = Field(
        default=None,
        title='URL Field',
        description='A field for the URL',
    )
