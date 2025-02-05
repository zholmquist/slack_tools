import json
from dataclasses import asdict, dataclass, is_dataclass
from typing import Callable, Self

from slack_tools.actions.handler import ActionHandler
from slack_tools.blocks.blocks import (
    ActionsBlock,
    AnyBlock,
    ContextBlock,
    DividerBlock,
    HeaderBlock,
    Image,
    RichPreformatted,
    RichQuote,
    RichSection,
    RichTextBlock,
    RichTextList,
    SectionBlock,
)
from slack_tools.blocks.interactive import (
    Button,
    Checkboxes,
    DatePicker,
    DateTimePicker,
    EmailInput,
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
from slack_tools.blocks.mixins.preview import BlockKitPreviewMixin
from slack_tools.blocks.objects import Option
from slack_tools.blocks.rich_text import (
    RichBroadcast,
    RichChannel,
    RichColor,
    RichDate,
    RichEmoji,
    RichLink,
    RichText,
    RichUser,
    RichUserGroup,
)
from slack_tools.blocks.text import MarkdownText, PlainText
from slack_tools.utils import remove_none


class BlockKitActions:
    action_handler: ActionHandler


@dataclass
class BlockKit(BlockKitActions, BlockKitPreviewMixin):
    """BlockKit Kit."""

    blocks: list[AnyBlock]

    def __init__(self, handler: ActionHandler | None = None):
        self.blocks = []

        self.action_handler = handler if handler else ActionHandler()

        # Objects
        self.option = Option.create
        self.image = Image.create

        # Elements
        self.plain_text = PlainText.create
        self.mrkdwn_text = MarkdownText.create

        # Rich Elements
        self.rich_broadcast = RichBroadcast.create
        self.rich_color = RichColor.create
        self.rich_channel = RichChannel.create
        self.rich_date = RichDate.create
        self.rich_emoji = RichEmoji.create
        self.rich_link = RichLink.create
        self.rich_text = RichText.create
        self.rich_user = RichUser.create
        self.rich_user_group = RichUserGroup.create

        # Interactive
        self.button = Button.create
        self.checkboxes = Checkboxes(options=[])

        # Inputs
        self.email_input = EmailInput.create
        self.plain_text_input = PlainTextInput.create
        self.url_input = URLInput.create
        self.number_input = NumberInput.create

        # Selects
        self.overflow_menu = OverflowMenu(options=[])
        self.radio_buttons = RadioButtons(options=[])
        self.static_select = StaticSelectMenu(options=[])
        self.static_multi_select = StaticMultiSelectMenu(options=[])
        self.external_select = ExternalSelectMenu(options=[])
        self.external_multi_select = ExternalMultiSelectMenu()
        self.user_select = UserSelectMenu()
        self.user_multi_select = UserMultiSelectMenu()
        self.conversation_select = ConversationSelectMenu()
        self.conversation_multi_select = ConversationMultiSelectMenu()
        self.channel_select = ChannelSelectMenu()
        self.channel_multi_select = ChannelMultiSelectMenu()

        # Date Pickers
        self.date_picker = DatePicker.create
        self.date_time_picker = DateTimePicker.create
        self.time_picker = TimePicker.create

        # Blocks
        self.actions = ActionsBlock(elements=[])
        self.context = ContextBlock(elements=[])
        self.divider = DividerBlock.create
        self.header = HeaderBlock.create
        self.section = SectionBlock.create
        self.rich_text_section = RichSection(elements=[])
        self.rich_text_list = RichTextList(elements=[])
        self.rich_text_preformatted = RichPreformatted(elements=[])
        self.rich_text_quote = RichQuote(elements=[])
        self.rich_text_block = RichTextBlock(elements=[])

    def get_callback_fn(self, action_id: str) -> Callable:
        if not self.action_handler:
            raise ValueError('Action handler not set')

        return self.action_handler.get_callback_callable(action_id)

    def __getitem__(self, blocks: AnyBlock | tuple[AnyBlock, ...]) -> Self:
        """Add blocks to the kit."""
        if not isinstance(blocks, tuple):
            blocks = (blocks,)

        for block in blocks:
            if hasattr(block, 'get_action') and callable(getattr(block, 'get_action')):
                callback = block.get_action()
                if callback:
                    self.action_handler.add_callback(
                        callback.action_id,
                        callback.callback,
                    )

        self.blocks.extend(blocks)
        return self

    def to_dict(self) -> dict:
        """Return dictionary representation."""
        if is_dataclass(self):
            block_dict = asdict(self)
        elif isinstance(self, dict):
            block_dict = self
        else:
            raise ValueError(f'Invalid type: {type(self)}')

        return remove_none(block_dict)

    def to_json(self, indent: int | None = None) -> str:
        """Return JSON string representation."""
        return json.dumps(self.to_dict(), indent=indent)

    def to_api(self) -> str:
        """Return JSON string representation for API."""
        render_blocks = self.to_dict()
        if 'blocks' in render_blocks:
            render_blocks = render_blocks['blocks']

        return json.dumps(render_blocks)
