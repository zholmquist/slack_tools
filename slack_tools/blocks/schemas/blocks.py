from dataclasses import dataclass
from typing import Literal

from slack_tools.blocks.schemas.base import BlockSchema
from slack_tools.blocks.schemas.elements import (
    AnyInteractiveElementSchema,
    AnyRichElementSchema,
)
from slack_tools.blocks.schemas.interactive import ButtonSchema
from slack_tools.blocks.schemas.objects import (
    MarkdownTextSchema,
    PlainTextSchema,
    SlackFileSchema,
)


@dataclass
class ImageSchema(BlockSchema, block_type='image'):
    """Image."""

    alt_text: str
    image_url: str | None = None
    slack_file: SlackFileSchema | None = None


@dataclass
class ActionsBlockSchema(BlockSchema, block_type='actions'):
    elements: list[AnyInteractiveElementSchema]


@dataclass
class ContextBlockSchema(BlockSchema, block_type='context'):
    """Context block."""

    elements: list[ImageSchema]


@dataclass
class DividerBlockSchema(BlockSchema, block_type='divider'):
    """Divider block."""

    pass


@dataclass
class FileSchema(BlockSchema, block_type='file'):
    """File."""

    external_id: str
    source: Literal['remote'] = 'remote'
    block_id: str | None = None


@dataclass
class HeaderBlockSchema(BlockSchema, block_type='header'):
    """Header block."""

    text: PlainTextSchema


@dataclass
class SectionBlockSchema(BlockSchema, block_type='section'):
    """Section block."""

    text: PlainTextSchema | MarkdownTextSchema
    accessory: ButtonSchema | ImageSchema | None = None

    # def get_action(self) -> ActionCallback | None:
    #     if self.accessory:
    #         return self.accessory.get_action()
    #     return None


class RichBlockSchema(BlockSchema):
    """Rich block."""

    pass


@dataclass
class RichSectionSchema(RichBlockSchema, block_type='rich_text_section'):
    """Rich text section."""

    elements: list[AnyRichElementSchema]


@dataclass
class RichTextListSchema(RichBlockSchema, block_type='rich_text_list'):
    """Rich text list."""

    elements: list[RichSectionSchema] | tuple[RichSectionSchema, ...]
    style: Literal['ordered', 'bullet'] = 'bullet'
    indent: int | None = None
    offset: int | None = None
    border: int | None = None


@dataclass
class RichPreformattedSchema(RichBlockSchema, block_type='rich_text_preformatted'):
    """Rich text preformatted."""

    elements: list[AnyRichElementSchema]
    border: int | None = None


@dataclass
class RichQuoteSchema(RichBlockSchema, block_type='rich_text_quote'):
    """Rich text quote."""

    elements: list[AnyRichElementSchema]
    border: int | None = None


@dataclass
class RichTextBlockSchema(BlockSchema, block_type='rich_text'):
    """Rich text block."""

    elements: list[
        RichSectionSchema
        | RichTextListSchema
        | RichPreformattedSchema
        | RichQuoteSchema
    ]
