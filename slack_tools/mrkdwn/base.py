from typing import Any

AnyItems = str | tuple[Any, ...] | list[Any]


class MarkdownStr(str):
    """Represents a Markdown String.

    This helps with parsing `str`'s from `MarkdownStr`'s.
    """

    pass


class SyntaxToken(MarkdownStr):
    """A Markdown Token (e.g., bold, italic, strikethrough).

    # TODO: Check for and escape characters: &, <, >
    """

    _template: str = '{}'  # default template

    def __new__(cls, value: str | None = None, /) -> 'SyntaxToken':
        return super().__new__(cls, cls._template.format(value))

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({super().__str__()})'
