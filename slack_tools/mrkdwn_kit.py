from slack_tools.mrkdwn import (
    H1,
    H2,
    H3,
    Bold,
    Code,
    CodeBlock,
    CodeInline,
    ComposeMarkdown,
    Italic,
    Link,
    List,
    MarkdownTable,
    Mention,
    Newline,
    Paragraph,
    Quote,
    Strikethrough,
    Todo,
)

__all__ = ['MarkdownKit']


class MarkdownKit:
    """Markdown utility with structured token types."""

    def __init__(self, extras: bool = False):
        """Extras are not supported in Slack."""
        self.bold = Bold
        self.italic = Italic
        self.strikethrough = Strikethrough
        self.new_line = Newline

        self.h1 = H1.create
        self.h2 = H2.create
        self.h3 = H3.create

        self.blockquote = Quote
        self.code_inline = CodeInline
        self.code_block = CodeBlock
        self.code = Code

        self.list = List

        self.link = Link
        self.email = Link
        self.mention = Mention
        self.compose = ComposeMarkdown

        if extras:
            self.table = MarkdownTable()
            self.todo = Todo.create
            self.p = Paragraph.create


md = MarkdownKit(extras=True)
