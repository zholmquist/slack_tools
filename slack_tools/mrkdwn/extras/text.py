from typing import Self

from slack_tools.mrkdwn.syntax import SyntaxToken


#
# Paragraph
#
class Paragraph(SyntaxToken):
    """A paragraph."""

    _template = '{}\n\n'

    def __new__(cls, value: str | None = None, /) -> Self:
        return super().__new__(cls, value)

    @classmethod
    def create(cls, value: str | None = None, /) -> Self:
        return cls(value)
