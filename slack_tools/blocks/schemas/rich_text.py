from dataclasses import dataclass
from typing import Literal

from slack_tools.blocks.schemas.base import BaseRichElement

__all__ = [
    'RichBroadcastSchema',
    'RichChannelSchema',
    'RichColorSchema',
    'RichDateSchema',
    'RichEmojiSchema',
    'RichLinkSchema',
    'RichTextSchema',
    'RichUserGroupSchema',
    'RichUserSchema',
    'StyleRichMentionSchema',
    'StyleRichTextSchema',
]


@dataclass
class StyleRichTextSchema:
    """Rich text style."""

    bold: bool = False
    italic: bool = False
    strike: bool = False
    code: bool = False


@dataclass
class StyleRichMentionSchema:
    """Rich mention style."""

    bold: bool = False
    italic: bool = False
    strike: bool = False
    highlight: bool = False
    client_highlight: bool = False
    unlink: bool = False


@dataclass
class RichBroadcastSchema(BaseRichElement, block_type='broadcast'):
    """Rich broadcast."""

    range: Literal['here', 'channel', 'everyone']


@dataclass
class RichColorSchema(BaseRichElement, block_type='color'):
    """Rich color."""

    color: str


@dataclass
class RichChannelSchema(BaseRichElement, block_type='channel'):
    """Rich channel."""

    channel_id: str
    style: StyleRichMentionSchema | None = None


@dataclass
class RichDateSchema(BaseRichElement, block_type='date'):
    """Rich date."""

    timestamp: int
    format: str
    url: str | None = None
    fallback: str | None = None


@dataclass
class RichEmojiSchema(BaseRichElement, block_type='emoji'):
    """Rich emoji."""

    name: str
    unicode: str | None = None


@dataclass
class RichLinkSchema(BaseRichElement, block_type='link'):
    """Rich link."""

    url: str
    text: str | None = None
    unsafe: bool = False
    style: StyleRichTextSchema | None = None


@dataclass
class RichTextSchema(BaseRichElement, block_type='text'):
    """Rich text."""

    text: str
    style: StyleRichTextSchema | None = None


@dataclass
class RichUserSchema(BaseRichElement, block_type='user'):
    """Rich user."""

    user_id: str
    style: StyleRichMentionSchema | None = None


@dataclass
class RichUserGroupSchema(BaseRichElement, block_type='usergroup'):
    """Rich user group."""

    user_group_id: str
    style: StyleRichMentionSchema | None = None
