from typing import Self

from slack_tools.blocks.schemas.objects import MarkdownTextSchema, PlainTextSchema
from slack_tools.mrkdwn.base import SyntaxToken

__all__ = ['MarkdownText', 'PlainText']


class PlainText(PlainTextSchema):
    """PlainText."""

    @classmethod
    def create(cls, text: str, /, *, emoji: bool = False) -> Self:
        return cls(text=text, emoji=emoji)


class MarkdownText(MarkdownTextSchema):
    """Markdown text block."""

    @classmethod
    def create(
        cls, text: str | SyntaxToken, /, *, verbatim: bool | None = None
    ) -> Self:
        return cls(text=text, verbatim=verbatim)
