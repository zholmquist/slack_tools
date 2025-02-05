import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Callable, Self

from slack_tools.blocks.base import (
    AnyDateType,
    BaseElement,
    ButtonStyle,
    InteractiveElement,
)
from slack_tools.blocks.mixins import (
    CallableElementMixin,
    CollectableElementMixin,
)
from slack_tools.blocks.objects import (
    ConfirmationDialog,
    DispatchActionConfig,
    Option,
    SlackFile,
)
from slack_tools.blocks.text import PlainText

# https://api.slack.com/reference/block-kit/block-elements#interactive-components


@dataclass
class Image(BaseElement, block_type='image'):
    """Image."""

    alt_text: str
    image_url: str | None = None
    slack_file: SlackFile | None = None

    @classmethod
    def create(cls, url: str, alt_text: str) -> Self:
        """Create an image block."""
        # TODO: Add SlackFile support
        return cls(image_url=url, alt_text=alt_text)


@dataclass
class ButtonSchema(
    InteractiveElement,
    block_type='button',
):
    """Button. Allows users a direct path to performing basic actions.

    [🔗 Documentation](https://api.slack.com/reference/block-kit/block-elements#button)
    """

    text: PlainText
    url: str | None = None
    style: ButtonStyle | None = None
    value: str | None = None
    accessibility_label: str | None = None
    action_id: str | None = None


@dataclass
class Button(CallableElementMixin, ButtonSchema):
    """Button."""

    @classmethod
    def create(
        cls,
        text: str,
        /,
        *,
        url: str | None = None,
        action_id: str | None = None,
        callback: Callable | None = None,
    ) -> Self:
        if action_id is None:
            action_id = str(uuid.uuid4())
        button = cls(
            text=PlainText(text=text),
            url=url,
            action_id=action_id,
        )
        if callback:
            button.action(callback)
        return button


#
# Collection block_block_type Elements
#
@dataclass
class Checkboxes(
    InteractiveElement,
    CollectableElementMixin[Option],
    block_type='checkboxes',
):
    """Checkbox Collection.

    [🔗 Documentation](https://api.slack.com/reference/block-kit/block-elements#checkboxes)
    """

    options: list[Option]
    initial_options: list[Option] | None = None
    confirm: ConfirmationDialog | None = None
    focus_on_load: bool | None = None
    action_id: str | None = None


@dataclass
class RadioButtons(
    InteractiveElement,
    CollectableElementMixin[Option],
    block_type='radio_buttons',
):
    """Radio Buttons.

    [🔗 Documentation](https://api.slack.com/reference/block-kit/block-elements#radio)
    """

    options: list[Option]
    initial_options: list[Option] | None = None
    action_id: str | None = None


#
# Input block_type Elements
#
@dataclass
class EmailInput(
    InteractiveElement,
    block_type='email_text_input',
):
    """Email Input."""

    dispatch_action_config: DispatchActionConfig | None = None
    initial_value: str | None = None
    focus_on_load: bool | None = None
    placeholder: PlainText | None = None
    action_id: str | None = None

    @classmethod
    def create(
        cls,
        initial_value: str | None = None,
        dispatch_action_config: dict | None = None,
        focus_on_load: bool | None = None,
        placeholder: str | None = None,
        action_id: str | None = None,
    ) -> Self:
        """Create an email input block."""
        return cls(
            initial_value=initial_value,
            dispatch_action_config=DispatchActionConfig(**dispatch_action_config)
            if dispatch_action_config
            else None,
            focus_on_load=focus_on_load,
            placeholder=PlainText(text=placeholder) if placeholder else None,
            action_id=action_id,
        )


@dataclass
class PlainTextInput(
    InteractiveElement,
    block_type='plain_text_input',
):
    """Plain Text Input."""

    multiline: bool = False
    min_length: int = 0
    max_length: int = 3000
    dispatch_action_config: DispatchActionConfig | None = None
    initial_value: str | None = None
    focus_on_load: bool | None = None
    placeholder: PlainText | None = None
    action_id: str | None = None

    @classmethod
    def create(
        cls,
        initial_value: str | None = None,
        dispatch_action_config: dict | None = None,
        focus_on_load: bool | None = None,
        placeholder: str | None = None,
        action_id: str | None = None,
    ) -> Self:
        """Create a plain text input block."""
        if action_id is None:
            action_id = str(uuid.uuid4())
        return cls(
            initial_value=initial_value,
            dispatch_action_config=DispatchActionConfig(**dispatch_action_config)
            if dispatch_action_config
            else None,
            focus_on_load=focus_on_load,
            placeholder=PlainText(text=placeholder) if placeholder else None,
            action_id=action_id,
        )


@dataclass
class URLInput(
    InteractiveElement,
    block_type='url_text_input',
):
    """URL Input."""

    dispatch_action_config: DispatchActionConfig | None = None
    initial_value: str | None = None
    focus_on_load: bool | None = None
    placeholder: PlainText | None = None
    action_id: str | None = None

    @classmethod
    def create(
        cls,
        initial_value: str | None = None,
        dispatch_action_config: dict | None = None,
        focus_on_load: bool | None = None,
        placeholder: str | None = None,
        action_id: str | None = None,
    ) -> Self:
        """Create a URL input block."""
        if action_id is None:
            action_id = str(uuid.uuid4())
        return cls(
            initial_value=initial_value,
            dispatch_action_config=DispatchActionConfig(**dispatch_action_config)
            if dispatch_action_config
            else None,
            focus_on_load=focus_on_load,
            placeholder=PlainText(text=placeholder) if placeholder else None,
            action_id=action_id,
        )


@dataclass
class NumberInput(
    InteractiveElement,
    block_type='number_input',
):
    """Number Input."""

    is_decimal_allowed: bool = False
    min_value: int | float | None = None
    max_value: int | float | None = None
    dispatch_action_config: DispatchActionConfig | None = None
    initial_value: str | None = None
    focus_on_load: bool | None = None
    placeholder: PlainText | None = None
    action_id: str | None = None

    @classmethod
    def create(
        cls,
        is_decimal_allowed: bool = False,
        min_value: int | float | None = None,
        max_value: int | float | None = None,
        dispatch_action_config: dict | None = None,
        initial_value: str | None = None,
        focus_on_load: bool | None = None,
        placeholder: str | None = None,
        action_id: str | None = None,
    ) -> Self:
        """Create a number input block."""
        if action_id is None:
            action_id = str(uuid.uuid4())
        return cls(
            is_decimal_allowed=is_decimal_allowed,
            min_value=min_value,
            max_value=max_value,
            dispatch_action_config=DispatchActionConfig(**dispatch_action_config)
            if dispatch_action_config
            else None,
            initial_value=initial_value,
            focus_on_load=focus_on_load,
            placeholder=PlainText(text=placeholder) if placeholder else None,
            action_id=action_id,
        )


#
# File block_block_type Element
#
@dataclass
class FileInput(
    InteractiveElement,
    block_type='file_input',
):
    """File Input."""

    file_types: str | None = None
    max_files: int = 10
    action_id: str | None = None

    @classmethod
    def create(
        cls,
        file_types: str | None = None,
        max_files: int = 10,
        action_id: str | None = None,
    ) -> Self:
        """Create a file input block."""
        if action_id is None:
            action_id = str(uuid.uuid4())
        return cls(file_types=file_types, max_files=max_files, action_id=action_id)


#
# Date and Time block_type Elements
#
@dataclass
class DatePicker(
    InteractiveElement,
    block_type='datepicker',
):
    """Datepicker."""

    initial_date: datetime | None = None
    confirm: ConfirmationDialog | None = None
    focus_on_load: bool | None = None
    placeholder: PlainText | None = None

    @classmethod
    def create(
        cls,
        initial_date: AnyDateType | None = None,
        placeholder: str | None = None,
        focus_on_load: bool | None = None,
    ) -> Self:
        """Create a datepicker."""
        if placeholder:
            placeholder = PlainText(text=placeholder)  # type: ignore

        return cls(
            initial_date=initial_date,  # type: ignore
            placeholder=placeholder,  # type: ignore
            focus_on_load=focus_on_load,
        )


@dataclass
class DateTimePicker(
    InteractiveElement,
    block_type='datetimepicker',
):
    """DateTime Picker."""

    initial_date: datetime | None = None
    confirm: ConfirmationDialog | None = None
    focus_on_load: bool | None = None

    @classmethod
    def create(
        cls,
        initial_date: AnyDateType | None = None,
        placeholder: str | None = None,
        focus_on_load: bool | None = None,
    ) -> Self:
        """Create a datetimepicker."""
        placeholder_text: PlainText | None = None
        if placeholder:
            placeholder_text = PlainText(text=placeholder)

        return cls(
            initial_date=initial_date,  # type: ignore
            placeholder=placeholder_text,
            focus_on_load=focus_on_load,
        )


@dataclass
class TimePicker(
    InteractiveElement,
    block_type='timepicker',
):
    """Time Picker."""

    initial_time: str | None = None
    confirm: ConfirmationDialog | None = None
    focus_on_load: bool | None = None
    placeholder: PlainText | None = None
    timezone: str | None = None  # A string in the IANA format, e.g. "America/Chicago".

    @classmethod
    def create(
        cls,
        initial_time: str | None = None,
        placeholder: str | None = None,
        focus_on_load: bool | None = None,
    ) -> Self:
        """Create a timepicker."""
        if placeholder:
            placeholder = PlainText(text=placeholder)

        return cls(
            initial_time=initial_time,
            placeholder=placeholder,
            focus_on_load=focus_on_load,
        )
