from dataclasses import dataclass
from typing import Annotated, Self, override

from slack_tools.blocks.base import BaseBlock
from slack_tools.mrkdwn.base import SyntaxToken
from slack_tools.utils import contains_emoji
from slack_tools.validators.rules import Constraints

__all__ = ['MarkdownText', 'PlainText']


@dataclass
class PlainText(BaseBlock, block_type='plain_text'):
    """PlainText."""

    text: Annotated[str, Constraints(min_length=1, max_length=3000)]
    emoji: bool = False

    def __post_init__(self):
        if contains_emoji(self.text):
            self.emoji = True

    @override
    def __str__(self) -> str:
        return self.text

    @classmethod
    def create(cls, text: str, /, *, emoji: bool = False) -> Self:
        return cls(text=text, emoji=emoji)


@dataclass
class MarkdownText(BaseBlock, block_type='mrkdwn'):
    """Markdown text block."""

    text: Annotated[str | SyntaxToken, Constraints(min_length=1, max_length=3000)]
    verbatim: bool | None = None

    def __post_init__(self):
        if isinstance(self.text, SyntaxToken):
            self.text = str(self.text)

    @classmethod
    def create(
        cls, text: str | SyntaxToken, /, *, verbatim: bool | None = None
    ) -> Self:
        return cls(text=text, verbatim=verbatim)
