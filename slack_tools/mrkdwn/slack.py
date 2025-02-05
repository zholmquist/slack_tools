from typing import Literal, Self

from slack_tools.mrkdwn.base import MarkdownStr, SyntaxToken
from slack_tools.mrkdwn.syntax import Bold, Italic, Strikethrough


class Stylizeable(MarkdownStr):
    """Apply markdown formatting to a whole string at once.

    [🔗 Documentation](https://api.slack.com/reference/surfaces/formatting#lists)
    """

    def __new__(cls, item: str) -> Self:
        return super().__new__(cls, item)

    def style(
        self, style: Literal['bold', 'italic', 'strikethrough'], /
    ) -> MarkdownStr:
        if style == 'bold':
            return self.bold()
        elif style == 'italic':
            return self.italic()
        elif style == 'strikethrough':
            return self.strikethrough()
        else:
            raise ValueError(f'Invalid style: {style}')

    def bold(self) -> MarkdownStr:
        return Bold(super().__str__())

    def italic(self) -> MarkdownStr:
        return Italic(super().__str__())

    def strikethrough(self) -> MarkdownStr:
        return Strikethrough(super().__str__())


class Link(SyntaxToken, Stylizeable):
    """A markdown-formatted link.

    [🔗 Documentation](https://api.slack.com/reference/surfaces/formatting#links)
    """

    _template = '<{}>'

    def __new__(cls, link: str, /, *items: str) -> Self:
        if '@' in link:
            link = f'mailto:{link}'
        if not items:
            return super(SyntaxToken, cls).__new__(cls, cls._template.format(link))
        return super(SyntaxToken, cls).__new__(
            cls, cls._template.format(f'{link}|{" ".join(items)}')
        )


class InternalLink(Link):
    """A markdown-formatted internal link.

    [🔗 Documentation](https://api.slack.com/reference/surfaces/formatting#links)
    """

    _symbol: str
    _template = '<{}{}>'

    def __new__(cls, entity: str) -> Self:
        if cls._symbol is None:
            raise ValueError('Symbol is not set')
        return super(SyntaxToken, cls).__new__(
            cls, cls._template.format(cls._symbol, entity)
        )


class BangMention(SyntaxToken):
    """A markdown-formatted mention.

    [🔗 Documentation](https://api.slack.com/reference/surfaces/formatting#mentions)
    """

    _template = '<!{}>'


class Mention(SyntaxToken):
    """A markdown-formatted mention.

    [🔗 Mentions Documentation](https://api.slack.com/reference/surfaces/formatting#mentions)
    """

    _template = '<{}>'

    @classmethod
    def _mention(cls, symbol: str, entity: str) -> Self:
        return super(SyntaxToken, cls).__new__(
            cls, cls._template.format(f'{symbol}{entity}')
        )

    @classmethod
    def _strip_symbol(cls, entity: str) -> str:
        return entity.lstrip('@#!')

    @classmethod
    def user(cls, entity: str) -> Self:
        """A markdown-formatted user mention.

        [🔗 Documentation](https://api.slack.com/reference/surfaces/formatting#linking-users)
        """
        return cls._mention('@', cls._strip_symbol(entity))

    @classmethod
    def channel(cls, entity: str | None = None) -> Self:
        """A markdown-formatted channel mention.

        Args:
            entity: Optional channel name/id. If None, returns a broadcast channel mention.

        [🔗 Documentation](https://api.slack.com/reference/surfaces/formatting#linking-channels)
        """
        if entity is None:
            return cls.broadcast('channel')
        return cls._mention('#', cls._strip_symbol(entity))

    @classmethod
    def group(cls, entity: str) -> Self:
        """A markdown-formatted user group mention.

        [🔗 Documentation](https://api.slack.com/reference/surfaces/formatting#linking-groups)
        """
        return cls._mention('!subteam^', cls._strip_symbol(entity))

    @classmethod
    def broadcast(cls, entity: str) -> Self:
        """Broadcast mention.

        [🔗 Documentation](https://api.slack.com/reference/surfaces/formatting#special-mentions)
        """
        return cls._mention('!', cls._strip_symbol(entity))

    @classmethod
    def everyone(cls) -> Self:
        """A markdown-formatted everyone mention."""
        return cls.broadcast('everyone')

    @classmethod
    def here(cls) -> Self:
        """A markdown-formatted here mention."""
        return cls.broadcast('here')
