from dataclasses import dataclass
from typing import Literal, Self

from slack_tools.blocks.base import BaseElement


class RichElement(BaseElement):
    pass


@dataclass
class RichBroadcast(RichElement, block_type='broadcast'):
    """Rich broadcast."""

    range: Literal['here', 'channel', 'everyone']

    @classmethod
    def create(cls, group: Literal['here', 'channel', 'everyone']) -> Self:
        return cls(range=group)


@dataclass
class RichColor(RichElement, block_type='color'):
    """Rich color."""

    color: str

    @classmethod
    def create(cls, color: str) -> Self:
        return cls(color=color)


@dataclass
class RichChannel(RichElement, block_type='channel'):
    """Rich channel."""

    channel_id: str
    style: (
        Literal['bold', 'italic', 'strike', 'highlight', 'client_highlight', 'unlink']
        | None
    ) = None

    @classmethod
    def create(
        cls,
        channel_id: str,
        /,
        *,
        style: Literal[
            'bold', 'italic', 'strike', 'highlight', 'client_highlight', 'unlink'
        ]
        | None = None,
    ) -> Self:
        return cls(channel_id=channel_id, style=style)


@dataclass
class RichDate(RichElement, block_type='date'):
    """Rich date."""

    timestamp: int
    format: str
    url: str | None = None
    fallback: str | None = None

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
        return cls(
            timestamp=timestamp, format=format_string, url=url, fallback=fallback
        )


@dataclass
class RichEmoji(RichElement, block_type='emoji'):
    """Rich emoji."""

    name: str
    unicode: str | None = None

    @classmethod
    def create(cls, name: str, /, *, unicode: str | None = None) -> Self:
        return cls(name=name, unicode=unicode)


@dataclass
class RichLink(RichElement, block_type='link'):
    """Rich link."""

    url: str
    text: str | None = None
    unsafe: bool = False
    style: Literal['bold', 'italic', 'strike', 'code'] | None = None

    @classmethod
    def create(
        cls,
        url: str,
        /,
        *,
        text: str | None = None,
        unsafe: bool = False,
        style: Literal['bold', 'italic', 'strike', 'code'] | None = None,
    ) -> Self:
        return cls(url=url, text=text, unsafe=unsafe, style=style)


@dataclass
class RichText(RichElement, block_type='text'):
    """Rich text."""

    text: str
    style: Literal['bold', 'italic', 'strike', 'code'] | None = None

    @classmethod
    def create(
        cls,
        text: str,
        /,
        *,
        style: Literal['bold', 'italic', 'strike', 'code'] | None = None,
    ) -> Self:
        return cls(text=text, style=style)


@dataclass
class RichUser(RichElement, block_type='user'):
    """Rich user."""

    user_id: str
    style: (
        Literal['bold', 'italic', 'strike', 'highlight', 'client_highlight', 'unlink']
        | None
    ) = None

    @classmethod
    def create(
        cls,
        user_id: str,
        /,
        *,
        style: Literal[
            'bold', 'italic', 'strike', 'highlight', 'client_highlight', 'unlink'
        ]
        | None = None,
    ) -> Self:
        return cls(user_id=user_id, style=style)


@dataclass
class RichUserGroup(RichElement, block_type='usergroup'):
    """Rich user group."""

    user_group_id: str
    style: (
        Literal['bold', 'italic', 'strike', 'highlight', 'client_highlight', 'unlink']
        | None
    ) = None

    @classmethod
    def create(
        cls,
        user_group_id: str,
        /,
        *,
        style: Literal[
            'bold', 'italic', 'strike', 'highlight', 'client_highlight', 'unlink'
        ]
        | None = None,
    ) -> Self:
        return cls(user_group_id=user_group_id, style=style)


AnyRichElement = (
    RichBroadcast
    | RichColor
    | RichChannel
    | RichDate
    | RichEmoji
    | RichLink
    | RichText
    | RichUser
    | RichUserGroup
)
