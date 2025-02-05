from typing import Literal, Self

from slack_tools.mrkdwn.syntax import SyntaxToken


#
# Headers
#
class HeaderBase(SyntaxToken):
    """Headers: #, ##, ###.

    *NOTE: Not supported by Slack.*
    """

    level: int = 1
    _render_as: Literal['inline', 'block'] = 'block'
    _template: str = '{}'  # placeholder, will be set in __new__

    def __new__(cls, value: str | None = None, /) -> Self:
        # Set the template based on level
        template = '\n\n' + ('#' * cls.level) + ' {}\n'
        instance = super().__new__(cls, template.format(value))
        return instance

    @classmethod
    def create(cls, value: str | None = None, /) -> Self:
        return cls(value)


class H1(HeaderBase):
    """Header 1: #."""

    level = 1


class H2(HeaderBase):
    """Header 2: ##."""

    level = 2


class H3(HeaderBase):
    """Header 3: ###."""

    level = 3


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
