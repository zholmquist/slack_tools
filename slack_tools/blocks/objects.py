from dataclasses import dataclass

from slack_tools.blocks.base import (
    BaseObject,
    ButtonStyle,
    ConversationTypes,
    KeyboardEvents,
)
from slack_tools.blocks.text import PlainText
from slack_tools.utils import is_url


@dataclass
class DispatchActionConfig(BaseObject):
    """Dispatch action config."""

    trigger_actions_on: list[KeyboardEvents]


@dataclass
class ConfirmationDialog(BaseObject):
    """Confirmation dialog."""

    title: PlainText
    text: PlainText
    confirm: PlainText
    deny: PlainText
    style: ButtonStyle | None = None


@dataclass
class Option(BaseObject):
    """Option block."""

    text: PlainText
    value: str
    description: PlainText | None = None
    url: str | None = None

    @classmethod
    def create(
        cls,
        text: str,
        /,
        *,
        value: str,
        description: str | None = None,
        url: str | None = None,
    ):  # -> Self:
        """Create an option block."""
        return cls(
            text=PlainText(text=text),
            value=value,
            description=PlainText(text=description) if description else None,
            url=url,
        )


@dataclass
class OptionGroup(BaseObject):
    """Option Group Block: A group of options in a select menu.

    [🔗 Documentation](https://api.slack.com/reference/block-kit/blocks#option_group)
    """

    label: PlainText

    options: list[Option]


@dataclass
class ConversationFilter(BaseObject):
    """Filter."""

    include: list[ConversationTypes] | None = None
    exclude_external_shared_channels: bool = False
    exclude_bot_users: bool = False


@dataclass
class FileObject(BaseObject):
    """File object."""

    id: str | None = None
    url: str | None = None

    def __str__(self) -> str:
        return self.to_json()


class SlackFile:
    """Helper class to create a FileObject.

    Note: Currently only png, jpg, jpeg, and gif Slack image files are supported.
    """

    def __new__(
        cls,
        value: str | None = None,
        /,
        *,
        url: str | None = None,
        slack_id: str | None = None,
    ):
        if value is not None:
            if is_url(value):
                print('valid url')
                return FileObject(url=value)
            return FileObject(id=value)
        return FileObject(url=url, id=slack_id)
