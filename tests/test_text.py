from dataclasses import asdict

from slack_tools.blocks.text import MarkdownText, PlainText


def test_plain_text():
    """Test the PlainText class."""
    assert asdict(PlainText('Hello')) == {
        'text': 'Hello',
        'type': 'plain_text',
        'emoji': False,
    }


def test_markdown_text():
    """Test the MarkdownText class."""
    assert asdict(MarkdownText('Hello')) == {
        'text': 'Hello',
        'type': 'mrkdwn',
        'verbatim': None,
    }


def test_plain_text_create():
    """Test the PlainText create method."""
    assert PlainText.create('Hello') == PlainText('Hello')
    assert PlainText.create('Hello', emoji=True) == PlainText('Hello', emoji=True)


def test_markdown_text_create():
    """Test the MarkdownText create method."""
    assert MarkdownText.create('Hello') == MarkdownText('Hello')
    assert MarkdownText.create('Hello', verbatim=True) == MarkdownText(
        'Hello', verbatim=True
    )
