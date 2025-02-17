"""Block Kit Schemas: Blocks.

Blocks are modular components that can be combined to create rich, interactive
messages within Slack apps. These classes help structure the JSON payloads
used when building Slack messages, modals, and Home tabs.

Blocks:
    - Actions Block
    - Context Block
    - Divider Block
    - File Block
    - Header Block
    - Image Block
    - Input Block
    - Markdown Block
    - Rich Text Block
    - Section Block
    - Video Block

References:
    - [🔗 Block Kit Documentation](https://api.slack.com/reference/block-kit/block)
"""

from dataclasses import dataclass, field
from typing import Final, Literal

from slack_tools.blocks.mixins.validator import TypeValidatorMixin
from slack_tools.blocks.schemas.base import BaseBlock, BaseRichBlock
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
from slack_tools.mrkdwn.extras.text import Paragraph
from slack_tools.mrkdwn.slack import Link
from slack_tools.mrkdwn.syntax import (
    H1,
    H2,
    H3,
    Bold,
    Code,
    CodeBlock,
    CodeInline,
    Italic,
    List,
    Newline,
    Quote,
    Strikethrough,
)


@dataclass
class ActionsBlockSchema(BaseBlock, block_type='actions'):
    """Actions Block.

    Holds multiple interactive elements.

    This block groups interactive components, allowing users to perform actions
    such as selecting options, picking dates, or triggering workflows.

    Surfaces:
        - Modals
        - Messages
        - Home

    Compatible Elements:
        - Button
        - Checkboxes
        - Date picker
        - Datetime picker
        - Multi-select menus
        - Overflow menu
        - Radio button
        - Rich text input
        - Select menu
        - Time picker
        - Workflow buttons

    References:
        - [🔗 Actions Block](https://api.slack.com/reference/block-kit/blocks#actions)
    """

    elements: list[AnyInteractiveElementSchema] = field(
        default_factory=list,
        metadata={
            'title': 'elements',
            'description': """
                An array of interactive element objects - buttons, select menus, overflow menus, or date pickers.
            """,
            'max_length': 25,
        },
    )


@dataclass
class ImageBlockSchema(BaseBlock, block_type='image'):
    """Image Block.

    Displays an image.

    An image block, designed to make those cat photos really pop.

    Validation:
        - Supported file types include png, jpg, jpeg, and gif.

    Surfaces:
        - Modals
        - Messages
        - Home

    Compatible Elements:
        None

    References:
        - [🔗 Image Block](https://api.slack.com/reference/block-kit/blocks#image)
    """

    _VALID_IMAGE_TYPES = ['png', 'jpg', 'jpeg', 'gif']

    alt_text: str = field(
        metadata={
            'title': 'alt_text',
            'description': 'A plain-text summary of the image. This should not contain any markup.',
            'max_length': 2000,
        },
    )
    image_url: str | None = field(
        default=None,
        metadata={
            'title': 'image_url',
            'description': 'The URL for a publicly hosted image. You must provide either an image_url or slack_file.',
            'max_length': 3000,
        },
    )
    slack_file: SlackFileSchema | None = field(
        default=None,
        metadata={
            'title': 'slack_file',
            'description': 'A Slack image file object that defines the source of the image.',
        },
    )
    title: PlainTextSchema | None = field(
        default=None,
        metadata={
            'title': 'title',
            'description': """
                An optional title for the image in the form of a text object
                that can only be of type: plain_text.
            """,
            'max_length': 2000,
        },
    )

    def __post_init__(self):
        """Validate image types."""
        if self.image_url and self.slack_file:
            raise ValueError('Only one of image_url or slack_file can be provided.')

        if self.image_url and not self.image_url.startswith('https://'):
            raise ValueError('image_url must start with https://')

        # check file types
        if self.slack_file and self.slack_file.source == 'remote':
            if self.slack_file.filetype not in self._VALID_IMAGE_TYPES:
                raise ValueError('Invalid file type.')


@dataclass
class ContextBlockSchema(BaseBlock, TypeValidatorMixin, block_type='context'):
    """Context Block.

    Displays contextual info, which can include both images and text.

    Surfaces:
        - Modals
        - Messages
        - Home

    Compatible Elements:
        - Image
        - Text

    References:
        - [🔗 Context Block](https://api.slack.com/reference/block-kit/blocks#context)
    """

    elements: list[ImageBlockSchema | MarkdownTextSchema | PlainTextSchema] = field(
        default_factory=list,
        metadata={
            'title': 'elements',
            'description': 'An array of image elements and text objects.',
            'max_length': 10,
        },
    )

    def __post_init__(self):
        """Validate elements types."""
        self.validate_field_type('elements')


@dataclass
class DividerBlockSchema(BaseBlock, block_type='divider'):
    """Divider Block.

    Visually separates pieces of info inside of a message.

    A content divider, like an <hr>, to split up different blocks inside of a message.
    The divider block is nice and neat, requiring only a type.

    Surfaces:
        - Modals
        - Messages
        - Home

    Compatible Elements:
        None

    References:
        - [🔗 Divider Block](https://api.slack.com/reference/block-kit/blocks#divider)
    """


@dataclass
class FileBlockSchema(BaseBlock, block_type='file'):
    """File Block.

    Displays a remote file.

    You can't add this block to app surfaces directly, but it will show up when
    retrieving messages that contain remote files.

    If you want to add remote files to messages, follow our guide.

    Surfaces:
        - Messages

    Compatible Elements:
        None

    References:
        - [🔗 File Block](https://api.slack.com/reference/block-kit/blocks#file)
    """

    # Required field must come first
    external_id: str = field(
        metadata={
            'title': 'external_id',
            'description': 'The external unique ID for this file.',
            'min_length': 1,
            'max_length': 255,
        },
    )

    # Optional fields with defaults after
    source: Final[Literal['remote']] = field(
        default='remote',
        metadata={
            'title': 'source',
            'description': 'At the moment, source will always be remote for a remote file.',
        },
    )


@dataclass
class HeaderBlockSchema(BaseBlock, block_type='header'):
    """Header block that displays a larger-sized text.

    This plain-text block renders in a larger, bold font and is used to delineate
    between different groups of content in your app's surfaces.

    Surfaces:
        - Modals
        - Messages
        - Home

    Compatible Elements:
        None

    References:
        - [🔗 Header Block](https://api.slack.com/reference/block-kit/blocks#header)
    """

    text: PlainTextSchema = field(
        metadata={
            'title': 'text',
            'description': 'The text for the block, in the form of a plain_text text object.',
            'max_length': 150,
        },
    )


@dataclass
class SectionBlockSchema(BaseBlock, TypeValidatorMixin, block_type='section'):
    """Section block for displaying text and interactive elements.

    This block displays text and can optionally include other block elements.
    It may be used alone as a text block, in combination with text fields, or
    side-by-side with certain interactive elements.

    Surfaces:
        - Modals
        - Messages
        - Home

    Compatible Elements:
        - Button
        - Checkboxes
        - Date picker
        - Image
        - Multi-select menus
        - Overflow menu
        - Radio button
        - Select menu
        - Time picker
        - Workflow buttons

    References:
        - [🔗 Section Block](https://api.slack.com/reference/block-kit/blocks#section)
    """

    text: PlainTextSchema | MarkdownTextSchema | None = field(
        default=None,
        metadata={
            'title': 'text',
            'description': 'The text for the block, in the form of a text object.',
            'min_length': 1,
            'max_length': 3000,
        },
    )

    accessory: ButtonSchema | ImageBlockSchema | None = field(
        default=None,
        metadata={
            'title': 'accessory',
            'description': 'One of compatible elements. Can be a `button`, `image`.',
        },
    )

    expand: bool = field(
        default=False,
        metadata={
            'title': 'expand',
            'description': """
                Whether or not this section block's text should always expand
                when rendered. If false or not provided, it may be rendered
                with a "see more" option to expand and show the full text.
                For AI Assistant apps, this allows the app to post long messages
                without users needing to click "see more" to expand the message.
            """,
        },
    )

    fields: list[PlainTextSchema] | None = field(
        default=None,
        metadata={
            'title': 'fields',
            'description': """
                Required if no text is provided. An array of text objects.
            """,
            'max_length': 10,
        },
    )

    def __post_init__(self):
        """Validate field types."""
        self.validate_field_type('text')
        self.validate_field_type('accessory')
        self.validate_field_type('fields')

        if self.text is None and self.fields is None:
            raise ValueError('text or fields is required.')

        if self.text and self.fields:
            raise ValueError('Only one of text or fields can be provided.')

        # Validate `field` contents
        if self.fields:
            for field in self.fields:
                if len(field.text) > 2000:
                    raise ValueError('Maximum length for the text in each item is 2000 characters.')


@dataclass
class InputBlockSchema(BaseBlock, block_type='input'):
    """Input Block.
    Collects information from users via block elements.

    Read our guides to collecting input in modals or in Home tabs to learn how
    input blocks pass information to your app.

    Surfaces:
        - Modals
        - Messages
        - Home tabs

    Compatible Elements:
        - Checkboxes
        - Date picker
        - Datetime picker
        - Email input
        - File input
        - Multi-select menus
        - Number input
        - Plain-text input
        - Radio button
        - Rich text input
        - Select menu
        - Time picker
        - URL input
    """

    label: PlainTextSchema = field(
        metadata={
            'title': 'label',
            'description': """
                The label text for the block, in the form of a plain_text text object.
                Maximum length for the text in this field is 2000 characters.
            """,
            'max_length': 2000,
        },
    )

    element: AnyInteractiveElementSchema = field(
        metadata={
            'title': 'element',
            'description': """
                A block element. See above for full list.
            """,
        },
    )

    dispatch_action: bool = field(
        default=False,
        metadata={
            'title': 'dispatch_action',
            'description': """
                A boolean that indicates whether or not the use of elements in
                this block should dispatch a block_actions payload. This field
                is incompatible with the file_input block element. If dispatch_action
                is set to true and a file_input block element is provided, an
                unsupported type error will be raised.
            """,
        },
    )

    hint: PlainTextSchema | None = field(
        default=None,
        metadata={
            'title': 'hint',
            'description': 'An optional hint that appears below an input element in a lighter grey.',
            'max_length': 2000,
        },
    )

    optional: bool = field(
        default=False,
        metadata={
            'title': 'optional',
            'description': """
                A boolean that indicates whether the input element may be empty
                when a user submits the modal.
            """,
        },
    )


@dataclass
class MarkdownBlockSchema(BaseBlock, block_type='markdown'):
    """Markdown block.

    Displays formatted markdown.

    This block can be used with AI apps when you expect a markdown response
    from an LLM that can get lost in translation rendering in Slack. Providing
    it in a markdown block leaves the translating to Slack to ensure your message
    appears as intended.

    Note:
        - Passing a single block may result in multiple blocks after translation.
        - The markdown types that are not supported are code block with syntax
            highlighting, horizontal lines, tables, and task list.

    Surfaces:
        - Messages

    Compatible Elements:
        None

    References:
        - [🔗 Markdown Block](https://api.slack.com/reference/block-kit/blocks#markdown)
        - [🔗 Supported Markdown](https://api.slack.com/reference/block-kit/blocks#rich_fields)
    """

    text: (
        str
        | Bold
        | Italic
        | Strikethrough
        | Newline
        | Quote
        | CodeInline
        | CodeBlock
        | Code
        | List
        | Link
        | Paragraph
        | H1
        | H2
        | H3
        # | Mention - ?
        # ! | Image - TODO!
    ) = field(
        metadata={
            'title': 'text',
            'description': 'The standard markdown-formatted text. Limit 12,000 characters max.',
            'max_length': 12000,
        },
    )


@dataclass
class RichSectionSchema(BaseRichBlock, block_type='rich_text_section'):
    """Rich text section."""

    elements: list[AnyRichElementSchema] = field(
        default_factory=list,
        metadata={
            'title': 'elements',
            'description': 'An array of rich text elements.',
        },
    )


@dataclass
class RichTextListSchema(BaseRichBlock, block_type='rich_text_list'):
    """Rich text list."""

    def __post_init__(self):
        if self.indent is not None and self.indent > 8:
            raise ValueError('indent must be less than 8.')

    elements: list[RichSectionSchema] | tuple[RichSectionSchema, ...] = field(
        default_factory=list,
        metadata={
            'title': 'elements',
            'description': """
                An array of rich text section objects containing two properties:
                - type, which is "rich_text_section"
                - elements, which is an array of rich text element objects.
            """,
        },
    )
    style: Literal['ordered', 'bullet'] | None = field(
        default=None,
        metadata={
            'title': 'style',
            'description': """
                Either bullet or ordered, the latter meaning a numbered list.
            """,
        },
    )
    indent: int | None = field(
        default=None,
        metadata={
            'title': 'indent',
            'description': 'Number of pixels to indent the list. Less than 8.',
        },
    )
    offset: int | None = field(
        default=None,
        metadata={
            'title': 'offset',
            'description': 'Number of pixels to offset the list.',
        },
    )
    border: int | None = field(
        default=None,
        metadata={
            'title': 'border',
            'description': 'Number of pixels of border thickness.',
        },
    )


@dataclass
class RichPreformattedSchema(BaseRichBlock, block_type='rich_text_preformatted'):
    """Rich text preformatted."""

    elements: list[AnyRichElementSchema] = field(
        default_factory=list,
        metadata={
            'title': 'elements',
            'description': 'An array of rich text elements.',
        },
    )
    border: int | None = field(
        default=None,
        metadata={
            'title': 'border',
            'description': 'Number of pixels of border thickness.',
        },
    )


@dataclass
class RichQuoteSchema(BaseRichBlock, block_type='rich_text_quote'):
    """Rich text quote."""

    elements: list[AnyRichElementSchema] = field(
        default_factory=list,
        metadata={
            'title': 'elements',
            'description': 'An array of rich text elements.',
        },
    )
    border: int | None = field(
        default=None,
        metadata={
            'title': 'border',
            'description': 'Number of pixels of border thickness.',
        },
    )


@dataclass
class RichTextBlockSchema(BaseBlock, block_type='rich_text'):
    """Rich Text Block.

    Displays formatted, structured representation of text.

    It is also the output of the Slack client's WYSIWYG message composer,
    so all messages sent by end-users will have this format. Use this block to
    include user-defined formatted text in your Block Kit payload. While it is
    possible to format text with mrkdwn, rich_text is strongly preferred and
    allows greater flexibility.

    You might encounter a rich_text block in a message payload, as a built-in
    type in workflow apps, or as output of the rich_text_input block element.

    Rich text blocks can be deeply nested. For instance: a rich_text_list can
    contain a rich_text_section which can contain bold style text.

    Sub-elements are what comprise the elements array in a rich text block.
    There are four available rich text object sub-elements.:
        - rich_text_section
        - rich_text_list
        - rich_text_preformatted
        - rich_text_quote

    Available Surfaces:
        - Messages
        - Modals
        - Home

    Compatible Elements:
        - rich_text_section
        - rich_text_list
        - rich_text_preformatted
        - rich_text_quote

    References:
        - [🔗 Rich Text Block](https://api.slack.com/reference/block-kit/blocks#rich_text)
    """

    elements: list[RichSectionSchema | RichTextListSchema | RichPreformattedSchema | RichQuoteSchema] = field(
        default_factory=list,
        metadata={
            'title': 'elements',
            'description': 'An array of rich text objects:',
        },
    )


@dataclass
class VideoBlockSchema(BaseBlock, block_type='video'):
    """Video block for embedding video content in Slack.

    Displays an embedded video player within Slack app surfaces, including
    messages, modals, link unfurls, and Home tabs. This block requires
    specific app scopes and URL constraints to function properly.

    Requirements:
        - Only apps can post video blocks; users cannot post them directly.
        - The app must have the `links.embed:write` scope for both user and bot tokens.
        - `video_url` must be included in the unfurl domains specified in your app settings.
        - `video_url` should be publicly accessible unless access control is handled via Events API payloads.
        - Must be compatible with embeddable iFrames, returning a 2xx status
            (or up to 5 redirects with an eventual 2xx).
        - Cannot point to Slack-related domains.

    Constraints:
        - Embeddable video players only (audio-only content is permitted).
        - No navigation, scrolling, or overlays allowed within the iFrame.
        - Interactivity (likes, comments, reactions) is allowed but must not
            fully overlay or navigate away from the content.
        - Interactive features will be anonymous, as no user data is transferred to the embedded view.

    Surfaces:
        - Modals
        - Messages
        - Home tabs

    Compatible Elements:
        None

    References:
        - [🔗 Video Block](https://api.slack.com/reference/block-kit/blocks#video)
    """

    title: PlainTextSchema = field(
        metadata={
            'title': 'title',
            'description': """
                Video title in the form of a text object that must have type of plain_text.
                text within must be less than 200 characters.
            """,
            'max_length': 200,
        },
    )

    thumbnail_url: str = field(
        metadata={
            'title': 'thumbnail_url',
            'description': 'The thumbnail image URL',
        },
    )

    video_url: str = field(
        metadata={
            'title': 'video_url',
            'description': """
                The URL to be embedded. Must match any existing unfurl domains
                within the app and point to a HTTPS URL.
            """,
        },
    )

    alt_text: str = field(
        init=False,
        metadata={
            'title': 'alt_text',
            'description': 'A tooltip for the video. Required for accessibility',
        },
    )

    author_name: str | None = field(
        default=None,
        metadata={
            'title': 'author_name',
            'description': 'Author name to be displayed. Must be less than 50 characters.',
            'max_length': 50,
        },
    )

    title_url: str | None = field(
        default=None,
        metadata={
            'title': 'title_url',
            'description': """
                Hyperlink for the title text. Must correspond to the non-embeddable
                URL for the video. Must go to an HTTPS URL.
            """,
        },
    )

    description: PlainTextSchema | None = field(
        default=None,
        metadata={
            'title': 'description',
            'description': """
                Description for video in the form of a text object that must have type of plain_text.
                text within must be less than 200 characters.
            """,
            'max_length': 200,
        },
    )

    provider_icon_url: str | None = field(
        default=None,
        metadata={
            'title': 'provider_icon_url',
            'description': 'Icon for the video provider, e.g. YouTube icon.',
        },
    )

    provider_name: str | None = field(
        default=None,
        metadata={
            'title': 'provider_name',
            'description': 'The originating application or domain of the video, e.g. YouTube.',
        },
    )
