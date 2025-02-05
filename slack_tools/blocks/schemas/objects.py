from dataclasses import dataclass

from slack_tools.blocks.schemas.base import ObjectSchema
from slack_tools.blocks.schemas.type_defs import (
    ButtonStyle,
    ConversationType,
    KeyboardEvent,
)
from slack_tools.mrkdwn.base import SyntaxToken
from slack_tools.utils import contains_emoji
from slack_tools.utils.dataclass_utils import Field


@dataclass
class PlainTextSchema(ObjectSchema, block_type='plain_text'):
    """Plain Text: Defines an object containing some text.

    [🔗 Documentation](https://api.slack.com/reference/block-kit/composition-objects#text)
    """

    text: str = Field(
        title='text',
        description="""
        """,
    )
    emoji: bool = False

    def __post_init__(self):
        if contains_emoji(self.text):
            self.emoji = True

    def __str__(self) -> str:
        return self.text


@dataclass
class MarkdownTextSchema(ObjectSchema, block_type='mrkdwn'):
    """Markdown Text: Defines an object containing some text.

    [🔗 Documentation](https://api.slack.com/reference/block-kit/composition-objects#text)
    """

    text: str
    verbatim: bool | None = None

    def __post_init__(self):
        if isinstance(self.text, SyntaxToken):
            self.text = str(self.text)


@dataclass
class ConfirmationDialogSchema(ObjectSchema):
    """Confirmation Dialog: A confirmation dialog step.

    [🔗 Documentation](https://api.slack.com/reference/block-kit/composition-objects#confirm)
    """

    title: PlainTextSchema
    text: PlainTextSchema
    confirm: PlainTextSchema
    deny: PlainTextSchema
    style: ButtonStyle | None = 'primary'


@dataclass
class ConversationFilterSchema(ObjectSchema):
    """Filter."""

    include: list[ConversationType] | None = None
    exclude_external_shared_channels: bool = False
    exclude_bot_users: bool = False


@dataclass
class DispatchActionConfigSchema(ObjectSchema):
    """Dispatch action config.

    [🔗 Documentation](https://api.slack.com/reference/block-kit/composition-objects#dispatch_action_config)
    """

    trigger_actions_on: list[KeyboardEvent]


@dataclass
class OptionSchema(ObjectSchema):
    """Option: An item in a number of item selection elements.

    [🔗 Documentation](https://api.slack.com/reference/block-kit/composition-objects#option)
    """

    text: PlainTextSchema
    value: str
    description: PlainTextSchema | None = None
    url: str | None = None


@dataclass
class OptionGroupSchema(ObjectSchema):
    """Option Group: Defines a way to group options in a menu.



    [🔗 Documentation](https://api.slack.com/reference/block-kit/blocks#option_group)
    """

    label: PlainTextSchema
    options: list[OptionSchema]


@dataclass
class SlackFileSchema(ObjectSchema):
    """Slack File object.

    [🔗 Documentation](https://api.slack.com/reference/block-kit/composition-objects#slack_file)
    """

    id: str | None = None
    url: str | None = None

    @property
    def filetype(self) -> str:
        if self.url:
            return self.url.split('.')[-1]
        return self.id.split('.')[-1]
