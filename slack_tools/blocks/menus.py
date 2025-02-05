from dataclasses import dataclass

from slack_tools.blocks.base import InteractiveElement
from slack_tools.blocks.mixins.collectable import CollectableElementMixin
from slack_tools.blocks.objects import (
    ConfirmationDialog,
    ConversationFilter,
    Option,
    OptionGroup,
)
from slack_tools.blocks.text import PlainText


@dataclass
class OverflowMenu(
    InteractiveElement,
    CollectableElementMixin[Option],
    block_type='overflow',
):
    """Overflow Menu."""

    options: list[Option]
    confirm: ConfirmationDialog | None = None
    action_id: str | None = None


@dataclass
class StaticMultiSelectMenu(
    InteractiveElement,
    CollectableElementMixin[Option],
    block_type='static_select',
):
    """Static Multi-Select Menu."""

    options: list[Option]
    option_groups: list[OptionGroup] | None = None
    initial_options: list[Option] | None = None

    confirm: ConfirmationDialog | None = None
    max_selected_items: int | None = None
    focus_on_load: bool | None = None
    placeholder: PlainText | None = None
    action_id: str | None = None


@dataclass
class StaticSelectMenu(
    InteractiveElement,
    CollectableElementMixin[Option],
    block_type='multi_static_select',
):
    """Static Multi-Select Menu."""

    options: list[Option]
    option_groups: list[OptionGroup] | None = None
    initial_option: Option | None = None

    confirm: ConfirmationDialog | None = None
    max_selected_items: int | None = None
    focus_on_load: bool | None = None
    placeholder: PlainText | None = None
    action_id: str | None = None


@dataclass
class ExternalSelectMenu(
    InteractiveElement,
    CollectableElementMixin[Option],
    block_type='external_select',
):
    """External Select Menu."""

    options: list[Option]
    option_groups: list[OptionGroup] | None = None
    min_query_length: int = 3
    initial_option: Option | None = None

    confirm: ConfirmationDialog | None = None
    max_selected_items: int | None = None
    focus_on_load: bool | None = None
    placeholder: PlainText | None = None
    action_id: str | None = None


@dataclass
class ExternalMultiSelectMenu(
    InteractiveElement,
    CollectableElementMixin[Option],
    block_type='multi_external_select',
):
    """External Static Multi-Select Menu."""

    initial_options: list[Option] | None = None
    min_query_length: int = 3

    confirm: ConfirmationDialog | None = None
    max_selected_items: int | None = None
    focus_on_load: bool | None = None
    placeholder: PlainText | None = None
    action_id: str | None = None


@dataclass
class UserSelectMenu(
    InteractiveElement,
    CollectableElementMixin[Option],
    block_type='users_select',
):
    """User Select Menu."""

    initial_user: str | None = None

    confirm: ConfirmationDialog | None = None
    max_selected_items: int | None = None
    focus_on_load: bool | None = None
    placeholder: PlainText | None = None
    action_id: str | None = None


@dataclass
class UserMultiSelectMenu(
    InteractiveElement,
    CollectableElementMixin[Option],
    block_type='multi_users_select',
):
    """User Multi-Select Menu."""

    initial_users: list[str] | None = None

    confirm: ConfirmationDialog | None = None
    max_selected_items: int | None = None
    focus_on_load: bool | None = None
    placeholder: PlainText | None = None
    action_id: str | None = None


@dataclass
class ConversationSelectMenu(
    InteractiveElement,
    CollectableElementMixin[Option],
    block_type='conversations_select',
):
    """Conversation Select Menu."""

    initial_conversation: str | None = None
    default_to_current_conversation: bool | None = None
    # Why None? If default_to_current_conversation is also supplied, initial_conversation will be ignored.
    response_url_enabled: bool = False
    filter: ConversationFilter | None = None

    confirm: ConfirmationDialog | None = None
    max_selected_items: int | None = None
    focus_on_load: bool | None = None
    placeholder: PlainText | None = None
    action_id: str | None = None


@dataclass
class ConversationMultiSelectMenu(
    InteractiveElement,
    CollectableElementMixin[Option],
    block_type='multi_conversations_select',
):
    """Conversation Multi-Select Menu."""

    initial_conversations: list[str] | None = None
    default_to_current_conversation: bool | None = None
    # Why None? If default_to_current_conversation is also supplied, initial_conversations will be ignored.
    filter: ConversationFilter | None = None

    confirm: ConfirmationDialog | None = None
    max_selected_items: int | None = None
    focus_on_load: bool | None = None
    placeholder: PlainText | None = None
    action_id: str | None = None


@dataclass
class ChannelSelectMenu(
    InteractiveElement,
    CollectableElementMixin[Option],
    block_type='channels_select',
):
    """Channel Select Menu."""

    initial_channel: str | None = None
    response_url_enabled: bool = False

    confirm: ConfirmationDialog | None = None
    max_selected_items: int | None = None
    focus_on_load: bool | None = None
    placeholder: PlainText | None = None
    action_id: str | None = None


@dataclass
class ChannelMultiSelectMenu(
    InteractiveElement,
    CollectableElementMixin[Option],
    block_type='multi_channels_select',
):
    """Channel Multi-Select Menu."""

    initial_channels: list[str] | None = None

    confirm: ConfirmationDialog | None = None
    max_selected_items: int | None = None
    focus_on_load: bool | None = None
    placeholder: PlainText | None = None
    action_id: str | None = None
