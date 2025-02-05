"""Block Kit Schemas: Base.

Base classes for Block Kit schemas.
"""

from dataclasses import dataclass, field

from slack_tools.blocks.mixins.serializable import SerializableMixin
from slack_tools.blocks.schemas.block_metaclass import BlockMetaclass


class BaseSchema(SerializableMixin):
    """Base class for Block Kit schemas.

    This is where it all starts. Every schema in Block Kit builds on top of this,
    ensuring that everything plays nicely with Slack's structure.
    """


class BaseObject(BaseSchema, metaclass=BlockMetaclass):
    """Base class for Block Kit `Composition Objects`.

    Think of these as the ingredients inside Blocks and Elements.
    They hold properties and data, making everything come together.

    References:
        - [🔗 Block Kit Composition Objects](https://api.slack.com/reference/block-kit#composition-objects)
    """


class BaseElement(BaseSchema, metaclass=BlockMetaclass):
    """Base class for Block Kit `Elements`.

    Elements are the small but mighty building blocks of a Slack UI.
    Buttons, input fields, and other interactive bits fall into this category.

    References:
        - [🔗 Block Kit Elements](https://api.slack.com/reference/block-kit#elements)
    """


class BaseInteractiveElement(BaseElement):
    """Base class for `Interactive Elements`.

    These are the elements that users can actually click, type in, or interact with.
    If something in your UI needs user input, it's probably in this class.

    References:
        - [🔗 Block Kit Interactive Elements](https://api.slack.com/reference/block-kit#interactive-elements)
    """


class BaseRichElement(BaseElement):
    """Base class for `Rich Elements`.

    Need to add some flair? Rich Elements help you style and format your blocks
    to look more polished and engaging.

    References:
        - [🔗 Block Kit Rich Elements](https://api.slack.com/reference/block-kit#rich-elements)
    """


class BaseLayout(BaseSchema, metaclass=BlockMetaclass):
    """Base class for `Layout` components.

    This is where we start organizing things. Layouts help structure blocks
    and elements into meaningful groups. In Slack's world, these are called `Blocks`.

    If you're building a more complex UI, this is your foundation.

    """


@dataclass
class BaseBlock(BaseLayout, metaclass=BlockMetaclass):
    """Base class for `Blocks`.

    Blocks are the fundamental pieces that make up a Slack app's UI.
    Every message or interactive view is made up of one or more blocks.

    References:
        - [🔗 Block Kit Blocks](https://api.slack.com/reference/block-kit#blocks)
    """

    block_id: str | None = field(
        default=None,
        init=False,
        metadata={
            'title': 'block_id',
            'description': 'A string acting as a unique identifier for a block.',
            'max_length': 255,
        },
    )


class BaseRichBlock(BaseBlock):
    """Base class for `Rich Blocks`.

    If you want to take your blocks to the next level with richer formatting,
    this is your go-to.

    References:
        - [🔗 Block Kit Rich Blocks](https://api.slack.com/reference/block-kit/blocks#rich)
    """


class BaseSurface(BaseSchema, metaclass=BlockMetaclass):
    """Base class for `Surfaces`.

    A Surface is the big container that holds everything together.
    Think of it as the Slack message or modal that displays your blocks.

    References:
        - [🔗 Block Kit Surfaces](https://api.slack.com/reference/block-kit/surfaces)
    """
