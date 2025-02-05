import pytest

from slack_tools.mrkdwn.syntax import (
    Bold,
    Code,
    CodeBlock,
    CodeInline,
    Italic,
    List,
    Newline,
    Quote,
    Strikethrough,
)


@pytest.mark.parametrize(
    'syntax_class,input_text,expected',
    [
        (Bold, 'Hello', '*Hello*'),
        (Bold, '', '**'),
        (Bold, '*Special*', '**Special**'),
        (Italic, 'Hello', '_Hello_'),
        (Italic, '', '__'),
        (Strikethrough, 'Hello', '~Hello~'),
        (Strikethrough, '', '~~'),
    ],
)
def test_basic_syntax(syntax_class, input_text, expected):
    """Test basic inline markdown syntax with various inputs."""
    assert str(syntax_class(input_text)) == expected


def test_newline():
    """Test newline behavior."""
    assert str(Newline()) == '\n'
    assert str(Newline() + Newline()) == '\n\n'


@pytest.mark.parametrize(
    'input_text,expected',
    [
        ('Hello', '> Hello\n'),
        ('Multi\nLine', '> Multi\nLine\n'),  # Actual behavior: only prefixes first line
        ('', '> \n'),  # Actual behavior: includes space
    ],
)
def test_quote(input_text, expected):
    """Test quote formatting with various inputs."""
    assert str(Quote(input_text)) == expected


class TestCode:
    """Group all code-related tests together."""

    @pytest.mark.parametrize(
        'input_text,expected',
        [
            ('Hello', '`Hello`'),
            ('', '``'),
            ('`backticks`', '``backticks``'),  # Actual behavior: doubles backticks
        ],
    )
    def test_inline(self, input_text, expected):
        """Test inline code formatting."""
        assert str(CodeInline(input_text)) == expected

    @pytest.mark.parametrize(
        'input_text,language,expected',
        [
            ('Hello', None, '```\nHello\n```'),
            ('Hello', 'python', '```python\nHello\n```'),
            ('', 'python', '```python\n\n```'),
        ],
    )
    def test_block(self, input_text, language, expected):
        """Test code block formatting with and without language specification."""
        assert str(CodeBlock(input_text, language=language)) == expected

    def test_code_shorthand(self):
        """Test the Code shorthand behavior."""
        assert str(Code('Hello')) == '`Hello`'
        assert str(Code('Hello', language='python')) == '`Hello`'
        assert (
            str(Code(['Hello', 'World'], language='python'))
            == '```python\nHello\nWorld\n```'
        )


class TestList:
    """Group all list-related tests together."""

    @pytest.mark.parametrize(
        'items,style,expected',
        [
            (['Hello', 'World'], None, '- Hello\n- World'),
            (['Hello', 'World'], ['*', '*'], '* Hello\n* World'),
            ([], None, ''),
            (['Hello', ['World', '!']], None, '- Hello\n- World\n\t* !'),
        ],
    )
    def test_list_formatting(self, items, style, expected):
        """Test list formatting with various configurations."""
        assert str(List(items, style=style)) == expected
