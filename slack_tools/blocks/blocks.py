from typing import Any, Literal, Self, Sequence, TypeAlias

from slack_tools.actions.schemas import ActionCallback
from slack_tools.blocks.interactive import (
    Button,
    Checkboxes,
    DatePicker,
    DateTimePicker,
    EmailInput,
    FileInput,
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
from slack_tools.blocks.rich_text import AnyRichElement, RichText
from slack_tools.blocks.schemas.blocks import (
    ActionsBlockSchema,
    ContextBlockSchema,
    DividerBlockSchema,
    HeaderBlockSchema,
    ImageBlockSchema,
    RichPreformattedSchema,
    RichQuoteSchema,
    RichSectionSchema,
    RichTextBlockSchema,
    RichTextListSchema,
    SectionBlockSchema,
)
from slack_tools.blocks.schemas.rich_text import StyleRichTextSchema
from slack_tools.blocks.text import MarkdownText, PlainText
from slack_tools.mrkdwn.base import MarkdownStr, SyntaxToken
from slack_tools.mrkdwn.syntax import Bold, CodeInline, Italic, Strikethrough

AnyElement = (
    # Interactive
    Button
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


class Image(ImageBlockSchema):
    @classmethod
    def create(
        cls,
        alt_text: str,
        /,
        *,
        image_url: str | None = None,
    ) -> Self:
        return cls(alt_text=alt_text, image_url=image_url)


class ActionsBlock(ActionsBlockSchema, CollectableElementMixin[ElementType]):
    @classmethod
    def create(cls, elements: list[ElementType]) -> Self:
        return cls(elements=elements)


class ContextBlock(ContextBlockSchema, CollectableElementMixin[ElementType]):
    @classmethod
    def create(cls, elements: list[ElementType]) -> Self:
        return cls(elements=elements)


class DividerBlock(DividerBlockSchema):
    @classmethod
    def create(cls) -> Self:
        return cls()


class HeaderBlock(HeaderBlockSchema):
    @classmethod
    def create(cls, text: str) -> Self:
        return cls(text=PlainText(text=text))


class SectionBlock(SectionBlockSchema):
    @classmethod
    def create(
        cls,
        text: str | SyntaxToken,
        /,
        *,
        accessory: Button | None = None,  # Image
    ) -> Self:
        """Create a section block."""
        # print(isinstance(text, SyntaxToken))
        if isinstance(text, MarkdownStr) or isinstance(text, SyntaxToken):
            text = MarkdownText(text=text)
        else:
            text = PlainText(text=text)
        return cls(text=text, accessory=accessory)

    def get_action(self) -> ActionCallback | None:
        if self.accessory and isinstance(self.accessory, Button):
            return self.accessory.get_action()
        return None


class RichSection(RichSectionSchema, CollectableElementMixin[AnyRichElement]):
    @classmethod
    def create(cls, elements: list[AnyRichElement]) -> Self:
        if isinstance(elements, MarkdownStr) or isinstance(elements, SyntaxToken):
            elements = MarkdownText(text=elements)
        else:
            elements = PlainText(text=elements)
        return cls(elements=elements)

    def __getitem__(
        self: Self,
        elements: AnyRichElement | tuple[AnyRichElement, ...] | list[AnyRichElement],
    ) -> Self:
        """Add items to the designated collection field."""
        if isinstance(elements, tuple):
            elements = list(elements)
        elif not isinstance(elements, list):
            elements = [elements]

        new_elements = []
        for element in elements:
            if isinstance(element, MarkdownStr) or isinstance(element, SyntaxToken):
                style_flags = {}
                if isinstance(element, Bold):
                    style_flags['bold'] = True
                if isinstance(element, Italic):
                    style_flags['italic'] = True
                if isinstance(element, Strikethrough):
                    style_flags['strike'] = True
                if isinstance(element, CodeInline):
                    style_flags['code'] = True

                new_elements.append(
                    RichText(
                        element.sanitize(),
                        style=StyleRichTextSchema(**style_flags),
                    ),
                )
            elif isinstance(element, str):
                new_elements.append(RichText(element))
            else:
                new_elements.append(element)

        return self.__class__(**{'elements': new_elements})


class StyleBlock:
    def __init__(self, value: Any):
        self.value = value

    def styles(
        self,
        ordered: bool | None = None,
        indent: int | None = None,
        offset: int | None = None,
        border: int | None = None,
    ):
        if indent is not None and indent > 8:
            raise ValueError('indent must be less than 8.')

        self.value.style = 'ordered' if ordered else 'bullet'
        self.value.indent = indent
        self.value.offset = offset
        self.value.border = border

        return self.value


class RichTextList(RichTextListSchema, StyleBlock):
    @classmethod
    def create(
        cls,
        elements: list[RichSection],
        /,
        *,
        style: Literal['ordered', 'bullet'] = 'bullet',
        indent: int | None = None,
        offset: int | None = None,
        border: int | None = None,
    ) -> Self:
        return cls(elements=elements, style=style, indent=indent, offset=offset, border=border)

    def __getitem__(self: Self, items: RichSection | tuple[RichSection, ...] | list[RichSection]) -> Self:
        """Add items to the designated collection field."""
        if isinstance(items, tuple):
            items = list(items)
        elif not isinstance(items, list):
            items = [items]
        return StyleBlock(self.__class__(**{'elements': items}))


class RichPreformatted(RichPreformattedSchema, CollectableElementMixin[AnyRichElement]):
    @classmethod
    def create(
        cls,
        elements: list[AnyRichElement],
        /,
        *,
        border: int | None = None,
    ) -> Self:
        return cls(elements=elements, border=border)


class RichQuote(RichQuoteSchema, CollectableElementMixin[AnyRichElement]):
    @classmethod
    def create(
        cls,
        elements: list[AnyRichElement],
        /,
        *,
        border: int | None = None,
    ) -> Self:
        return cls(elements=elements, border=border)


AnyRichBlock = RichSection | RichTextList | RichPreformatted | RichQuote


class RichTextBlock(RichTextBlockSchema, CollectableElementMixin[AnyRichBlock]):
    @classmethod
    def create(cls, elements: list[AnyRichBlock]) -> Self:
        return cls(elements=elements)


AnyBlock = (
    Image
    | ActionsBlock
    | ContextBlock
    | DividerBlock
    | HeaderBlock
    | SectionBlock
    | RichSection
    | RichTextList
    | RichPreformatted
    | RichQuote
    | RichTextBlock
)
