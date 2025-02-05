from typing import Self

from slack_tools.mrkdwn.base import MarkdownStr


class TodoGlyph(MarkdownStr):
    """Todo glyphs."""

    open = MarkdownStr(' ')
    done = MarkdownStr('x')


class Todo(MarkdownStr):
    _done: bool = False
    _template = '[{}]'
    _humanize = False

    def __new__(
        cls,
        glyph: TodoGlyph | str = TodoGlyph.open,
        *,
        done: bool = False,
        humanize: bool = False,
    ) -> Self:
        instance = super().__new__(
            cls,
            'Yes'
            if (done and humanize)
            else 'No'
            if humanize
            else cls._template.format(glyph),
        )
        instance.is_done = done
        return instance

    @property
    def is_done(self) -> bool:
        return self._done

    @is_done.setter
    def is_done(self, value: bool) -> None:
        self._done = value

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({super().__str__()})'

    @classmethod
    def create(
        cls, glyph: TodoGlyph | str = TodoGlyph.open, *, humanize: bool = False
    ) -> Self:
        if isinstance(glyph, str):
            glyph = TodoGlyph.done if glyph == 'x' else TodoGlyph.open
        return cls(glyph, humanize=humanize)

    def done(self) -> Self:
        return self.__class__(
            TodoGlyph.done,
            done=True,
            humanize=isinstance(self, str) and self in ('Yes', 'No'),
        )

    def humanize(self) -> str:
        return 'Yes' if self.is_done else 'No'
