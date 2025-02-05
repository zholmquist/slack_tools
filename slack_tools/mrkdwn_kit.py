from slack_tools.mrkdwn.slack import Link, Mention
from slack_tools.mrkdwn.syntax import (
    Bold,
    Code,
    CodeBlock,
    CodeInline,
    ComposeMarkdown,
    Italic,
    List,
    Newline,
    Quote,
    Strikethrough,
)


class Markdown:
    """Markdown utility with structured token types."""

    bold = Bold
    italic = Italic
    strikethrough = Strikethrough
    new_line = Newline

    blockquote = Quote
    code_inline = CodeInline
    code_block = CodeBlock
    code = Code

    list = List

    # Links: URLs
    link = Link
    email = Link

    mention = Mention

    compose = ComposeMarkdown
