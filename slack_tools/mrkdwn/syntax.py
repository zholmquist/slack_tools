from typing import Literal, Self

from slack_tools.mrkdwn.base import AnyItems, MarkdownStr, SyntaxToken
from slack_tools.mrkdwn.glyphs import Glyph


class ListToken(MarkdownStr):
    """A markdown-formatted list with optional nesting and bullet styles."""

    def __new__(
        cls,
        items: list[AnyItems],
        style: list[MarkdownStr] | None = None,
    ) -> Self:
        """Create a markdown list with a multi-level bullet style."""
        default_style = [Glyph.dash, Glyph.asterisk, Glyph.circle.open]
        style = style or default_style

        def _format_list(item, depth=0):
            indent_str = '\t' * depth
            bullet = style[min(depth, len(style) - 1)]
            if isinstance(item, (list, tuple)):
                parent, children = item[0], item[1:]
                parent_bullet = f'{indent_str}{bullet} {parent}'
                if children:
                    child_bullets = [
                        _format_list(child, depth + 1) for child in children
                    ]
                    return '\n'.join([parent_bullet] + child_bullets)
                return parent_bullet
            return f'{indent_str}{bullet} {item}'

        formatted_list = '\n'.join(_format_list(item) for item in items)
        return super().__new__(cls, formatted_list)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({super().__str__()})'


class LinkToken(MarkdownStr):
    """A markdown-formatted link."""

    def __new__(cls, url: str, *items: str) -> 'LinkToken':
        if not items:
            return super().__new__(cls, f'<{url}>')
        text = ' '.join(str(item) for item in items)
        return super().__new__(cls, f'<{url}|{text}>')

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({super().__str__()})'


class Bold(SyntaxToken):
    """A bold markdown token."""

    _template = '*{}*'


class Italic(SyntaxToken):
    """An italic markdown token."""

    _template = '_{}_'


class Strikethrough(SyntaxToken):
    """A strikethrough markdown token."""

    _template = '~{}~'


class Newline(SyntaxToken):
    """A newline markdown token.

    [🔗 Documentation](https://api.slack.com/reference/surfaces/formatting#line-breaks)
    """

    _template = '\n'


class Quote(SyntaxToken):
    """A quote markdown token.

    [🔗 Documentation](https://api.slack.com/reference/surfaces/formatting#quotes)
    """

    _template = '> {}\n'


class CodeInline(SyntaxToken):
    """A code inline markdown token.

    [🔗 Documentation](https://api.slack.com/reference/surfaces/formatting#inline-code)
    """

    _template = '`{}`'


class CodeBlock(SyntaxToken):
    """A code block markdown token.

    [🔗 Documentation](https://api.slack.com/reference/surfaces/formatting#inline-code)
    """

    _template = '```{}\n{}\n```'

    def __new__(cls, text: str, /, *, language: str | None = None) -> Self:
        formatted = (
            cls._template.format(language, text)
            if language
            else cls._template.format('', text)
        )
        instance = super(SyntaxToken, cls).__new__(cls, formatted)
        return instance


class Code(MarkdownStr):
    """A code markdown token.

    [🔗 Documentation](https://api.slack.com/reference/surfaces/formatting#inline-code)
    """

    def __new__(cls, text: str | list[str], /, *, language: str | None = None) -> Self:
        if isinstance(text, list):
            text = '\n'.join(text)
            return super().__new__(cls, CodeBlock(text, language=language))

        # Check if text starts with a language specification
        if isinstance(text, str) and text.startswith('```'):
            lines = text.split('\n', 1)
            if len(lines) > 1:
                language = lines[0].replace('```', '').strip()
                code = lines[1].rstrip('`').strip()
                return super().__new__(cls, CodeBlock(code, language=language))

        # If multiple lines use a block
        if '\n' in text:
            return super().__new__(cls, CodeBlock(text, language=language))
        return super().__new__(cls, CodeInline(text))


class List(MarkdownStr):
    """A markdown-formatted list.

    [🔗 Documentation](https://api.slack.com/reference/surfaces/formatting#lists)
    """

    def __new__(
        cls,
        items: list[AnyItems],
        /,
        *,
        style: list[MarkdownStr] | None = None,
    ) -> Self:
        return super().__new__(cls, ListToken(items, style))


class ComposeMarkdown(MarkdownStr):
    """A markdown-formatted content.

    [🔗 Documentation](https://api.slack.com/reference/surfaces/formatting#content)
    """

    def __new__(cls, *items: str) -> Self:
        # Convert items to strings and handle block vs inline elements
        formatted_items = []
        for item in items:
            # Check if item has _render_as attribute
            render_as = getattr(item, '_render_as', 'inline')
            str_item = str(item)

            if render_as == 'block':
                if formatted_items and not formatted_items[-1].endswith('\n'):
                    formatted_items.append('\n')
                formatted_items.append(str_item)
                if not str_item.endswith('\n'):
                    formatted_items.append('\n')
            else:
                # Inline element - join with space if needed
                if formatted_items and not formatted_items[-1].endswith('\n'):
                    formatted_items.append(' ')
                formatted_items.append(str_item)

        return super().__new__(cls, ''.join(formatted_items))

    def __str__(self) -> str:
        return super().__str__()
