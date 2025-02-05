from typing import Any, Literal

AnyItems = str | tuple[Any, ...] | list[Any]


class MarkdownStr(str):
    """Represents a Markdown String.

    This helps with parsing `str`'s from `MarkdownStr`'s.
    """

    pass


class SyntaxToken(MarkdownStr):
    """A Markdown Token (e.g., bold, italic, strikethrough)."""

    _render_as: Literal['inline', 'block'] = 'inline'
    _template: str = '{}'  # default template

    def __new__(cls, value: str | None = None, /) -> 'SyntaxToken':
        return super().__new__(cls, cls._template.format(value))

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({super().__str__()})'
