import uuid
from datetime import datetime
from typing import Callable, Self

from slack_tools.blocks.mixins import (
    CallableElementMixin,
    CollectableElementMixin,
)
from slack_tools.blocks.objects import Option
from slack_tools.blocks.schemas.interactive import (
    ButtonSchema,
    CheckboxesSchema,
    DatePickerSchema,
    DateTimePickerSchema,
    DispatchActionConfigSchema,
    EmailInputSchema,
    FileInputSchema,
    NumberInputSchema,
    PlainTextInputSchema,
    RadioButtonsSchema,
    TimePickerSchema,
    URLInputSchema,
)
from slack_tools.blocks.schemas.objects import PlainTextSchema


class Button(ButtonSchema, CallableElementMixin):
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
            text=PlainTextSchema(text=text),
            url=url,
            action_id=action_id,
        )
        if callback:
            button.action(callback)
        return button


class Checkboxes(CheckboxesSchema, CollectableElementMixin[Option]):
    """Checkboxes."""

    pass


class RadioButtons(RadioButtonsSchema, CollectableElementMixin[Option]):
    """Radio Buttons."""

    pass


class EmailInput(EmailInputSchema):
    """Email Input."""

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
            dispatch_action_config=DispatchActionConfigSchema(**dispatch_action_config)
            if dispatch_action_config
            else None,
            focus_on_load=focus_on_load,
            placeholder=PlainTextSchema(text=placeholder) if placeholder else None,
            action_id=action_id,
        )


class PlainTextInput(PlainTextInputSchema):
    """Plain Text Input."""

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
            dispatch_action_config=DispatchActionConfigSchema(**dispatch_action_config)
            if dispatch_action_config
            else None,
            focus_on_load=focus_on_load,
            placeholder=PlainTextSchema(text=placeholder) if placeholder else None,
            action_id=action_id,
        )


class URLInput(URLInputSchema):
    """URL Input."""

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
            dispatch_action_config=DispatchActionConfigSchema(**dispatch_action_config)
            if dispatch_action_config
            else None,
            focus_on_load=focus_on_load,
            placeholder=PlainTextSchema(text=placeholder) if placeholder else None,
            action_id=action_id,
        )


class NumberInput(NumberInputSchema):
    """Number Input."""

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
            dispatch_action_config=DispatchActionConfigSchema(**dispatch_action_config)
            if dispatch_action_config
            else None,
            initial_value=initial_value,
            focus_on_load=focus_on_load,
            placeholder=PlainTextSchema(text=placeholder) if placeholder else None,
            action_id=action_id,
        )


class FileInput(FileInputSchema):
    """File Input."""

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


class DatePicker(DatePickerSchema):
    """Datepicker."""

    @classmethod
    def create(
        cls,
        initial_date: str | int | datetime | None = None,
        placeholder: str | None = None,
        focus_on_load: bool | None = None,
    ) -> Self:
        """Create a datepicker."""
        if placeholder:
            placeholder = PlainTextSchema(text=placeholder)  # type: ignore

        return cls(
            initial_date=initial_date,  # type: ignore
            placeholder=placeholder,  # type: ignore
            focus_on_load=focus_on_load,
        )


class DateTimePicker(DateTimePickerSchema):
    """DateTime Picker."""

    @classmethod
    def create(
        cls,
        initial_date: str | int | datetime | None = None,
        placeholder: str | None = None,
        focus_on_load: bool | None = None,
    ) -> Self:
        """Create a datetimepicker."""
        placeholder_text: PlainTextSchema | None = None
        if placeholder:
            placeholder_text = PlainTextSchema(text=placeholder)

        return cls(
            initial_date=initial_date,  # type: ignore
            placeholder=placeholder_text,
            focus_on_load=focus_on_load,
        )


class TimePicker(TimePickerSchema):
    """Time Picker."""

    @classmethod
    def create(
        cls,
        initial_time: str | None = None,
        placeholder: str | None = None,
        focus_on_load: bool | None = None,
    ) -> Self:
        """Create a timepicker."""
        if placeholder:
            placeholder = PlainTextSchema(text=placeholder)

        return cls(
            initial_time=initial_time,
            placeholder=placeholder,
            focus_on_load=focus_on_load,
        )
