from slack_tools.blocks.schemas.interactive import (
    ButtonSchema,
    CheckboxesSchema,
    DatePickerSchema,
    DateTimePickerSchema,
    EmailInputSchema,
    FileInputSchema,
    NumberInputSchema,
    PlainTextInputSchema,
    RadioButtonsSchema,
    TimePickerSchema,
    URLInputSchema,
)
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
)

#
# Interactive Elements
#
AnyInteractiveElementSchema = (
    ButtonSchema
    | CheckboxesSchema
    | RadioButtonsSchema
    | EmailInputSchema
    | PlainTextInputSchema
    | URLInputSchema
    | NumberInputSchema
    | FileInputSchema
    | DatePickerSchema
    | DateTimePickerSchema
    | TimePickerSchema
)

#
# Rich Text Elements
#
AnyRichElementSchema = (
    RichBroadcastSchema
    | RichColorSchema
    | RichChannelSchema
    | RichDateSchema
    | RichEmojiSchema
    | RichLinkSchema
    | RichTextSchema
    | RichUserSchema
    | RichUserGroupSchema
)

#
# Any Element Schema
#
AnyElementSchema = AnyInteractiveElementSchema | AnyRichElementSchema
