from typing import Self

from slack_tools.mrkdwn.base import MarkdownStr


class VariantGlyph(MarkdownStr):
    """Base class for markdown-formatted bullet symbols with a default."""

    @classmethod
    def get_default(cls, default: str, /) -> MarkdownStr:
        """Returns the default variant."""
        return getattr(cls, default)


class Glyph(MarkdownStr):
    """A Glyph (bullet).

    Used to simplify list building with style.
    """

    none = MarkdownStr('')

    # basics
    dot = MarkdownStr('•')
    dash = MarkdownStr('-')
    asterisk = MarkdownStr('*')
    triangular = MarkdownStr('‣')
    leftward = MarkdownStr('⁌')
    rightward = MarkdownStr('⁍')

    class CircleVariant(VariantGlyph):
        filled = MarkdownStr('●')
        open = MarkdownStr('○')

    class ToDoVariant(VariantGlyph):
        filled = MarkdownStr('[x]')
        open = MarkdownStr('[ ]')
        checked = filled
        unchecked = open

    circle = CircleVariant
    todo = ToDoVariant

    def __new__(cls) -> Self:
        return super().__new__(cls, Glyph.dash)

    def __class_getitem__(cls, _) -> MarkdownStr:
        return cls.dash

    def __str__(cls) -> str:
        return str(cls.dash)

    def __repr__(cls) -> str:
        return str(cls.dash)
