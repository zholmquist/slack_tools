from dataclasses import dataclass
from datetime import datetime

from slack_tools.blocks.schemas.base import InteractiveElementSchema
from slack_tools.blocks.schemas.objects import (
    ButtonStyle,
    ConfirmationDialogSchema,
    DispatchActionConfigSchema,
    OptionSchema,
    PlainTextSchema,
)


@dataclass
class ButtonSchema(InteractiveElementSchema, block_type='button'):
    """Button. Allows users a direct path to performing basic actions.

    [🔗 Documentation](https://api.slack.com/reference/block-kit/block-elements#button)
    """

    text: PlainTextSchema
    url: str | None = None
    style: ButtonStyle | None = None
    value: str | None = None
    accessibility_label: str | None = None
    action_id: str | None = None


@dataclass
class CheckboxesSchema(InteractiveElementSchema, block_type='checkboxes'):
    """Checkbox Collection.

    [🔗 Documentation](https://api.slack.com/reference/block-kit/block-elements#checkboxes)
    """

    options: list[OptionSchema]
    initial_options: list[OptionSchema] | None = None
    confirm: ConfirmationDialogSchema | None = None
    focus_on_load: bool | None = None
    action_id: str | None = None


@dataclass
class RadioButtonsSchema(InteractiveElementSchema, block_type='radio_buttons'):
    """Radio Buttons.

    [🔗 Documentation](https://api.slack.com/reference/block-kit/block-elements#radio)
    """

    options: list[OptionSchema]
    initial_options: list[OptionSchema] | None = None
    action_id: str | None = None


@dataclass
class EmailInputSchema(InteractiveElementSchema, block_type='email_text_input'):
    """Email Input."""

    # dispatch_action_config: DispatchActionConfig | None = None
    initial_value: str | None = None
    focus_on_load: bool | None = None
    placeholder: PlainTextSchema | None = None
    action_id: str | None = None


@dataclass
class PlainTextInputSchema(InteractiveElementSchema, block_type='plain_text_input'):
    """Plain Text Input."""

    multiline: bool = False
    min_length: int = 0
    max_length: int = 3000
    dispatch_action_config: DispatchActionConfigSchema | None = None
    initial_value: str | None = None
    focus_on_load: bool | None = None
    placeholder: PlainTextSchema | None = None
    action_id: str | None = None


@dataclass
class URLInputSchema(InteractiveElementSchema, block_type='url_text_input'):
    """URL Input."""

    dispatch_action_config: DispatchActionConfigSchema | None = None
    initial_value: str | None = None
    focus_on_load: bool | None = None
    placeholder: PlainTextSchema | None = None
    action_id: str | None = None


@dataclass
class NumberInputSchema(InteractiveElementSchema, block_type='number_input'):
    """Number Input."""

    is_decimal_allowed: bool = False
    min_value: int | float | None = None
    max_value: int | float | None = None
    dispatch_action_config: DispatchActionConfigSchema | None = None
    initial_value: str | None = None
    focus_on_load: bool | None = None
    placeholder: PlainTextSchema | None = None
    action_id: str | None = None


#
# File block_block_type Element
#
@dataclass
class FileInputSchema(InteractiveElementSchema, block_type='file_input'):
    """File Input."""

    file_types: str | None = None
    max_files: int = 10
    action_id: str | None = None


#
# Date and Time block_type Elements
#
@dataclass
class DatePickerSchema(InteractiveElementSchema, block_type='datepicker'):
    """Datepicker."""

    initial_date: datetime | None = None
    confirm: ConfirmationDialogSchema | None = None
    focus_on_load: bool | None = None
    placeholder: PlainTextSchema | None = None


@dataclass
class DateTimePickerSchema(InteractiveElementSchema, block_type='datetimepicker'):
    """DateTime Picker."""

    initial_date: datetime | None = None
    confirm: ConfirmationDialogSchema | None = None
    focus_on_load: bool | None = None


@dataclass
class TimePickerSchema(InteractiveElementSchema, block_type='timepicker'):
    """Time Picker."""

    initial_time: str | None = None
    confirm: ConfirmationDialogSchema | None = None
    focus_on_load: bool | None = None
    placeholder: PlainTextSchema | None = None
    timezone: str | None = None  # A string in the IANA format, e.g. "America/Chicago".
