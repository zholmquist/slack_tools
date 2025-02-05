from dataclasses import dataclass
from typing import Literal, Self, Sequence, TypeAlias

from slack_tools.actions.schemas import ActionCallback
from slack_tools.blocks.base import BaseBlock
from slack_tools.blocks.interactive import (
    Button,
    Checkboxes,
    DatePicker,
    DateTimePicker,
    EmailInput,
    FileInput,
    Image,
    NumberInput,
    PlainTextInput,
    RadioButtons,
    TimePicker,
    URLInput,
)
from slack_tools.blocks.menus import (
    ChannelMultiSelectMenu,
    ChannelSelectMenu,
    ConversationMultiSelectMenu,
    ConversationSelectMenu,
    ExternalMultiSelectMenu,
    ExternalSelectMenu,
    OverflowMenu,
    StaticMultiSelectMenu,
    StaticSelectMenu,
    UserMultiSelectMenu,
    UserSelectMenu,
)
from slack_tools.blocks.mixins.collectable import CollectableElementMixin
from slack_tools.blocks.rich_text import AnyRichElement
from slack_tools.blocks.text import MarkdownText, PlainText
from slack_tools.mrkdwn.base import SyntaxToken

AnyElement = (
    Image
    # Interactive
    | Button
    | Checkboxes
    | DatePicker
    | DateTimePicker
    | TimePicker
    | OverflowMenu
    | EmailInput
    | FileInput
    | NumberInput
    | PlainTextInput
    | URLInput
    | RadioButtons
    # Select
    | StaticSelectMenu
    | ExternalSelectMenu
    | UserSelectMenu
    | ConversationSelectMenu
    | ChannelSelectMenu
    # Multi-Select
    | StaticMultiSelectMenu
    | ExternalMultiSelectMenu
    | UserMultiSelectMenu
    | ConversationMultiSelectMenu
    | ChannelMultiSelectMenu
)
ElementType: TypeAlias = AnyElement | Sequence[AnyElement] | tuple[AnyElement, ...]


@dataclass
class ActionsBlock(
    BaseBlock,
    CollectableElementMixin[ElementType],
    block_type='actions',
):
    elements: list[ElementType]


@dataclass
class ContextBlock(
    BaseBlock,
    CollectableElementMixin[ElementType],
    block_type='context',
):
    """Context block."""

    elements: list[Image]


@dataclass
class DividerBlock(BaseBlock, block_type='divider'):
    """Divider block."""

    @classmethod
    def create(cls) -> Self:
        """Create a divider block."""
        return cls()


@dataclass
class HeaderBlock(BaseBlock, block_type='header'):
    """Header block."""

    text: PlainText

    @classmethod
    def create(cls, text: str) -> Self:
        """Create a header block."""
        return cls(text=PlainText(text=text))


@dataclass
class SectionBlock(BaseBlock, block_type='section'):
    """Section block."""

    text: PlainText | MarkdownText
    accessory: Button | Image | None = None

    def get_action(self) -> ActionCallback | None:
        if self.accessory:
            return self.accessory.get_action()
        return None

    @classmethod
    def create(
        cls,
        text: str | SyntaxToken,
        /,
        *,
        accessory: Button | Image | None = None,
    ) -> Self:
        """Create a section block."""
        if isinstance(text, SyntaxToken):
            # Convert SyntaxToken to raw markdown string
            text = MarkdownText(text=text)
        else:
            text = PlainText(text=text)

        return cls(text=text, accessory=accessory)


class RichBlock(BaseBlock):
    """Rich block."""

    pass


@dataclass
class RichSection(
    RichBlock,
    CollectableElementMixin[AnyRichElement],
    block_type='rich_text_section',
):
    """Rich text section."""

    elements: list[AnyRichElement]


@dataclass
class RichTextList(
    RichBlock,
    CollectableElementMixin[RichSection],
    block_type='rich_text_list',
):
    """Rich text list."""

    elements: list[RichSection] | tuple[RichSection, ...]
    style: Literal['ordered', 'bullet'] = 'bullet'
    indent: int | None = None
    offset: int | None = None
    border: int | None = None


@dataclass
class RichPreformatted(
    RichBlock,
    CollectableElementMixin[AnyRichElement],
    block_type='rich_text_preformatted',
):
    """Rich text preformatted."""

    elements: list[AnyRichElement]
    border: int | None = None


@dataclass
class RichQuote(
    RichBlock,
    CollectableElementMixin[AnyRichElement],
    block_type='rich_text_quote',
):
    """Rich text quote."""

    elements: list[AnyRichElement]
    border: int | None = None


AnyRichBlock = RichSection | RichTextList | RichPreformatted | RichQuote


@dataclass
class RichTextBlock(
    BaseBlock,
    CollectableElementMixin[AnyRichBlock],
    block_type='rich_text',
):
    """Rich text block."""

    elements: list[AnyRichBlock]
