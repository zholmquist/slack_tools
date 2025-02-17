from typing import Literal, Self

from slack_tools.blocks.schemas.rich_text import (
    RichBroadcastSchema,
    RichChannelSchema,
    RichColorSchema,
    RichDateSchema,
    RichEmojiSchema,
    RichLinkSchema,
    RichTextSchema,
    RichUserGroupSchema,
    RichUserSchema,
    StyleRichMentionSchema,
    StyleRichTextSchema,
)
from slack_tools.mrkdwn.base import SyntaxToken


class RichBroadcast(RichBroadcastSchema):
    """Rich broadcast."""

    @classmethod
    def create(cls, group: Literal['here', 'channel', 'everyone']) -> Self:
        return cls(range=group)


class RichColor(RichColorSchema):
    """Rich color."""

    @classmethod
    def create(cls, color: str) -> Self:
        return cls(color=color)


class RichChannel(RichChannelSchema):
    """Rich channel."""

    @classmethod
    def create(
        cls,
        channel_id: str,
        /,
        *,
        style: StyleRichMentionSchema | None = None,
    ) -> Self:
        return cls(channel_id=channel_id, style=style)


class RichDate(RichDateSchema):
    """Rich date."""

    @classmethod
    def create(
        cls,
        timestamp: int,
        /,
        *,
        format_string: str,
        url: str | None = None,
        fallback: str | None = None,
    ) -> Self:
        return cls(timestamp=timestamp, format=format_string, url=url, fallback=fallback)


class RichEmoji(RichEmojiSchema):
    """Rich emoji."""

    @classmethod
    def create(cls, name: str, /, *, unicode: str | None = None) -> Self:
        return cls(name=name, unicode=unicode)


class RichLink(RichLinkSchema):
    """Rich link."""

    @classmethod
    def create(
        cls,
        url: str,
        /,
        *,
        text: str | None = None,
        unsafe: bool = False,
        style: StyleRichTextSchema | None = None,
    ) -> Self:
        return cls(url=url, text=text, unsafe=unsafe, style=style)


class RichText(RichTextSchema):
    """Rich text."""

    @classmethod
    def create(
        cls,
        text: str | SyntaxToken,
        /,
        *,
        style: StyleRichTextSchema | None = None,
    ) -> Self:
        return cls(text=text, style=style)


class RichUser(RichUserSchema):
    """Rich user."""

    @classmethod
    def create(
        cls,
        user_id: str,
        /,
        *,
        style: StyleRichMentionSchema | None = None,
    ) -> Self:
        return cls(user_id=user_id, style=style)


class RichUserGroup(RichUserGroupSchema):
    """Rich user group."""

    @classmethod
    def create(
        cls,
        user_group_id: str,
        /,
        *,
        style: StyleRichMentionSchema | None = None,
    ) -> Self:
        return cls(user_group_id=user_group_id, style=style)


AnyRichElement = (
    RichBroadcast | RichColor | RichChannel | RichDate | RichEmoji | RichLink | RichText | RichUser | RichUserGroup
)
